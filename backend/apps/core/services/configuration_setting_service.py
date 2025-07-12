from result import Result, Ok, Err

from apps.core.repositories import ConfigurationSettingRepository
from apps.core.types.logging_type import LoggingConfigKeysType, LoggingLevel


class ConfigurationSettingService:
    def __init__(self):
        self.repository = ConfigurationSettingRepository()

    def get_system_logging_level(self) -> str:
        """Get system logging level"""
        result = self.repository.find_one(key=LoggingConfigKeysType.SYSTEM_LOGGING_LEVEL)
        if result.is_err():
            return LoggingLevel.ERROR

        return result.ok_value.value

    def set_system_logging_level(self, level: LoggingLevel) -> Result[None, str]:
        """Set the system logging level"""
        try:
            result = self.repository.find_one(key=LoggingConfigKeysType.SYSTEM_LOGGING_LEVEL)

            if result.is_err():
                create_result = self.repository.create(data={
                    "key": LoggingConfigKeysType.SYSTEM_LOGGING_LEVEL,
                    "value": level
                })
                if create_result.is_err():
                    return Err(f"Error creating configuration setting: {create_result.err_value}")

                return Ok(None)
            else:
                update_result = self.repository.update(entity=result.ok_value, data={"value": level})
                if update_result.is_err():
                    return Err(f"Error updating configuration setting: {update_result.err_value}")
                return Ok(None)

        except Exception as e:
            return Err(f"Error setting system logging level: {str(e)}")

    def get_module_logging_level(self, module_name: str) -> str:
        """Get module logging level"""
        module_key = LoggingConfigKeysType.LOGGING_MODULE.format(module_name)
        result = self.repository.find_one(key=module_key)

        if result.is_err():
            return self.get_system_logging_level()

        return result.ok_value.value

    def set_module_logging_level(self, module_name: str, level: LoggingLevel) -> Result[None, str]:
        """Set the module logging level"""
        try:
            module_key = LoggingConfigKeysType.LOGGING_MODULE.format(module_name)
            result = self.repository.find_one(key=module_key)

            if result.is_err():
                create_result = self.repository.create(data={"key": module_key, "value": level})
                if create_result.is_err():
                    return Err(f"Error creating configuration setting: {create_result.err_value}")
                return Ok(None)
            else:
                update_result = self.repository.update(entity=result.ok_value, data={"value": level})
                if update_result.is_err():
                    return Err(f"Error updating configuration setting: {update_result.err_value}")
                return Ok(None)
        except Exception as e:
            return Err(f"Error setting module logging level: {str(e)}")
