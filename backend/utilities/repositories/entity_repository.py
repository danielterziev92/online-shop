from typing import Generic, TypeVar, List, Dict, Any, Optional, Union, Iterator, Type

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction, IntegrityError, OperationalError
from django.db.models import Model, QuerySet
from result import Result, Ok, Err
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from utilities.results.batch_result import BatchErrorResult, BulkResult

T = TypeVar("T", bound=Model)
ID = TypeVar("ID")


class EntityRepository(Generic[T, ID]):
    """Base a repository class with atomic transactions and deadlock prevention"""

    def __init__(self, model: Type[T], base_queryset: Optional[QuerySet[T]] = None):
        self.__model = model
        self.__base_queryset = base_queryset or self._create_default_queryset()

    @property
    def model(self) -> Type[T]:
        return self.__model

    @model.setter
    def model(self, value: Type[T]):
        if not issubclass(value, Model):
            raise TypeError("Model must be a subclass of django.db.models.Model")
        self.__model = value

    @property
    def base_queryset(self) -> QuerySet[T]:
        """Get the base queryset for all operations"""
        return self.__base_queryset

    @base_queryset.setter
    def base_queryset(self, value: QuerySet[T]):
        """Set a new base queryset"""
        self.__base_queryset = value

    def _create_default_queryset(self) -> QuerySet[T]:
        """Create the default queryset. Override this in subclasses for custom logic."""
        return self.model.objects.all()

    def get_by_id(self, entity_id: ID) -> Result[T, str]:
        """Get entity by id"""
        try:
            entity = self.base_queryset.get(id=entity_id)
            return Ok(entity)
        except ObjectDoesNotExist:
            return Err(f"Entity with id {entity_id} does not exist")
        except Exception as e:
            return Err(f"Error retrieving entity: {str(e)}")

    def find_one(self, **filters) -> Result[T, str]:
        """Find one record with given filters"""
        try:
            entity = self.base_queryset.get(**filters)
            return Ok(entity)
        except ObjectDoesNotExist:
            return Err(f"Entity with filters {filters} does not exist")
        except Exception as e:
            return Err(f"Error retrieving entity: {str(e)}")

    def find_all(self,
                 limit: int = 100,
                 offset: int = 0,
                 order_by: Optional[Union[str, List[str]]] = None,
                 distinct: bool = False,
                 select_related: Optional[Union[str, List[str]]] = None,
                 prefetch_related: Optional[Union[str, List[str]]] = None,
                 only: Optional[List[str]] = None,
                 defer: Optional[List[str]] = None,
                 **filters) -> Result[List[T], str]:
        """Find entities with advanced query options"""
        try:
            queryset = self.base_queryset.filter(**filters)

            if distinct:
                queryset = queryset.distinct()

            if select_related:
                if isinstance(select_related, str):
                    queryset = queryset.select_related(select_related)
                elif isinstance(select_related, list):
                    queryset = queryset.select_related(*select_related)

            if prefetch_related:
                if isinstance(prefetch_related, str):
                    queryset = queryset.prefetch_related(prefetch_related)
                elif isinstance(prefetch_related, list):
                    queryset = queryset.prefetch_related(*prefetch_related)

            if only:
                queryset = queryset.only(*only)

            if defer:
                queryset = queryset.defer(*defer)

            if order_by:
                if isinstance(order_by, str):
                    queryset = queryset.order_by(order_by)
                elif isinstance(order_by, list):
                    queryset = queryset.order_by(*order_by)

            return Ok(list(queryset[offset:offset + limit]))
        except Exception as e:
            return Err(f"Error retrieving entities: {str(e)}")

    def find_values(self,
                    values: List[str],
                    limit: int = 100,
                    offset: int = 0,
                    **filters) -> Result[List[Dict[str, Any]], str]:
        """Find entities returning only specific values as dictionaries"""
        try:
            queryset = self.base_queryset.filter(**filters).values(*values)
            return Ok(list(queryset[offset:offset + limit]))
        except Exception as e:
            return Err(f"Error retrieving values: {str(e)}")

    def find_values_list(self,
                         values: List[str],
                         flat: bool = False,
                         limit: int = 100,
                         offset: int = 0,
                         **filters) -> Result[List[Any], str]:
        """Find entities returning only specific values as tuples/lists"""
        try:
            queryset = self.base_queryset.filter(**filters).values_list(*values, flat=flat)
            return Ok(list(queryset[offset:offset + limit]))
        except Exception as e:
            return Err(f"Error retrieving values list: {str(e)}")

    def exists(self, **filters) -> bool:
        """Check if a record exists with given filters"""
        return self.base_queryset.filter(**filters).exists()

    def count(self, **filters) -> int:
        """Count records with given filters"""
        return self.base_queryset.filter(**filters).count()

    def create(self, data: Dict[str, Any]) -> Result[T, str]:
        """Create entity"""

        def create_entity():
            with transaction.atomic():
                obj = self.model(**data)
                obj.full_clean()
                obj.save()
                return obj

        try:
            entity = self._execute_with_retry(create_entity)
            return Ok(entity)
        except ValidationError as e:
            return Err(f"Validation error: {str(e)}")
        except IntegrityError as e:
            return Err(f"Integrity error: {str(e)}")
        except Exception as e:
            return Err(f"Error creating entity: {str(e)}")

    def update(self, entity: T, data: Dict[str, Any]) -> Result[T, str]:
        """Update record by entity"""

        def update_entity():
            with transaction.atomic():
                for key, value in data.items():
                    setattr(entity, key, value)
                entity.full_clean()
                entity.save()
                return entity

        try:
            updated_entity = self._execute_with_retry(update_entity)
            return Ok(updated_entity)
        except ValidationError as e:
            return Err(f"Validation error: {str(e)}")
        except Exception as e:
            return Err(f"Error updating entity: {str(e)}")

    def update_by_id(self, entity_id: ID, data: Dict[str, Any]) -> Result[T, str]:
        """Update record by id"""
        result = self.get_by_id(entity_id=entity_id)
        if result.is_err():
            return result
        return self.update(entity=result.ok_value, data=data)

    def delete(self, entity: T) -> Result[bool, str]:
        """Delete record by entity"""

        def delete_entity():
            with transaction.atomic():
                entity.delete()
                return True

        try:
            result = self._execute_with_retry(delete_entity)
            return Ok(result)
        except Exception as e:
            return Err(f"Error deleting entity: {str(e)}")

    def delete_by_id(self, entity_id: ID) -> Result[bool, str]:
        """Delete record by id"""
        result = self.get_by_id(entity_id=entity_id)
        if result.is_err():
            return result
        return self.delete(entity=result.ok_value)

    def bulk_create(self, data: List[Dict[str, Any]], batch_size: int = 1000) -> Result[List[T], BulkResult]:
        """Create multiple records in batches"""
        if not data:
            return Ok(list())

        if batch_size <= 0:
            return Err(BulkResult(entities=[], failed_batches=[BatchErrorResult(
                batch_index=0, batch_data=data, error_message="batch_size must be positive",
                error_type="ValueError", original_exception=ValueError("batch_size must be positive")
            )]))

        def create_entities(items: List[Dict[str, Any]]) -> List[T]:
            with transaction.atomic():
                objects_to_create = []
                for item in items:
                    obj = self.model(**item)
                    obj.full_clean()
                    objects_to_create.append(obj)

                return self.model.objects.bulk_create(objs=objects_to_create)

        successful_entities = list()
        failed_batches = list()

        for batch_index, batch_data in enumerate(self._batched(data=data, batch_size=batch_size)):
            try:
                entities = self._execute_with_retry(lambda: create_entities(batch_data))
                successful_entities.extend(entities)
            except Exception as e:
                failed_batches.append(BatchErrorResult(
                    batch_index=batch_index,
                    batch_data=batch_data,
                    error_message=str(e),
                    error_type=type(e).__name__,
                    original_exception=e
                ))

        if not failed_batches:
            return Ok(successful_entities)

        return Err(BulkResult(entities=successful_entities, failed_batches=failed_batches))

    def bulk_update(self,
                    entities: List[T],
                    data: Dict[str, Any],
                    batch_size: int = 1000,
                    validate: bool = True) -> Result[List[T], BulkResult]:
        """Update multiple entities with the same data."""
        if not entities:
            return Ok(list())

        if batch_size <= 0:
            return Err(BulkResult(entities=[], failed_batches=[BatchErrorResult(
                batch_index=0, batch_data=entities, error_message="batch_size must be positive",
                error_type="ValueError", original_exception=ValueError("batch_size must be positive")
            )]))

        def update_entities(items: List[T], update_data: Dict[str, Any]) -> int:
            with transaction.atomic():
                for item in items:
                    for field, value in update_data.items():
                        setattr(item, field, value)
                    if validate:
                        item.full_clean()

                return self.model.objects.bulk_update(
                    objs=items,
                    fields=list(update_data.keys()),
                    batch_size=len(items)
                )

        successful_entities = list()
        failed_batches = list()

        for batch_index, batch_data in enumerate(self._batched(entities, batch_size=batch_size)):
            try:
                self._execute_with_retry(lambda: update_entities(batch_data, data))
                successful_entities.extend(batch_data)
            except Exception as e:
                failed_batches.append(BatchErrorResult(
                    batch_index=batch_index,
                    batch_data=batch_data,
                    error_message=str(e),
                    error_type=type(e).__name__,
                    original_exception=e
                ))

        if not failed_batches:
            return Ok(successful_entities)

        return Err(BulkResult(entities=successful_entities, failed_batches=failed_batches))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=0.1, max=2),
        retry=retry_if_exception_type((IntegrityError, OperationalError)),
        reraise=True)
    def _execute_with_retry(self, operation_func, *args, **kwargs):
        """Execute a batch operation with retry logic for deadlocks"""
        return operation_func(*args, **kwargs)

    @staticmethod
    def _batched(data: List[Any], batch_size: int = 1000) -> Iterator[List[Any]]:
        """Generator that yields a batch of data"""
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")

        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]
