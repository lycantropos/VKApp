class VKObject:
    def download(self, save_path: str):
        """Must be overridden by inheritors"""

    @classmethod
    def name(cls) -> str:
        """
        For elements of attachments (such as VK photo, audio objects) should return their key in attachment object
        e.g. for VK photo object should return 'photo', for VK audio object should return 'audio' and etc.
        """

    @classmethod
    def get_vk_objects_from_raw(cls, raw_vk_objects: list) -> list:
        vk_objects = list(
            cls.from_raw(raw_vk_object)
            for raw_vk_object in raw_vk_objects
        )
        return vk_objects

    @classmethod
    def from_raw(cls, raw_vk_object: dict):
        """Must be overridden by inheritors"""
