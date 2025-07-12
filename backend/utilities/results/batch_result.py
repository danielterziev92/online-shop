from typing import List, Any

from pydantic.dataclasses import dataclass


@dataclass
class BatchErrorResult:
    """Information about a failed batch"""
    batch_index: int
    batch_data: List[Any]
    error_message: str
    error_type: str
    original_exception: Exception


@dataclass
class BulkResult:
    """Result object containing information about bulk operation failures"""
    entities: List[Any]
    failed_batches: List[BatchErrorResult]

    @property
    def has_failures(self) -> bool:
        return len(self.failed_batches) > 0

    @property
    def successful_count(self) -> int:
        return len(self.entities)

    @property
    def total_failed_count(self) -> int:
        return len(self.failed_batches)
