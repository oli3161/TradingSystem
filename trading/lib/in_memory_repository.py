class InMemoryRepository[T]:
    def __init__(self):
        self._data: dict[int, T] = {}
        self._id_counter: int = 1

    def add(self, item: T) -> int:
        item_id = self._id_counter
        self._data[item_id] = item
        self._id_counter += 1

        return item_id

    def get(self, item_id: int) -> T | None:
        return self._data.get(item_id)

    def get_all(self) -> list[T]:
        return list(self._data.values())

    def update(self, item_id: int, new_item: T) -> bool:
        if item_id in self._data:
            self._data[item_id] = new_item
            return True

        return False

    def delete(self, item_id: int) -> bool:
        if item_id in self._data:
            del self._data[item_id]
            return True

        return False

    def count(self) -> int:
        return len(self._data)
