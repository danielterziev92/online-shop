from apps.core.models import ConfigurationSetting
from utilities.repositories import EntityRepository


class ConfigurationSettingRepository(EntityRepository[ConfigurationSetting, int]):
    def __init__(self):
        super().__init__(ConfigurationSetting)
        