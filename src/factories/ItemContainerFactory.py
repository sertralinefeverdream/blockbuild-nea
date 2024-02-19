from items.ItemContainer import ItemContainer
from items.HotbarContainer import HotbarContainer

#uploaded

class ItemContainerFactory:
    def __init__(self):
        pass

    def create_item_container(self, container_id, *args, state_data=None, **kwargs):
        item_container = None

        if container_id.lower() == "item_container":
            item_container = ItemContainer(*args, **kwargs)
        elif container_id.lower() == "hotbar_container":
            item_container = HotbarContainer(*args, **kwargs)

        if state_data is not None:
            item_container.load_from_data(state_data)

        return item_container
