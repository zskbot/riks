from collections import defaultdict
from datetime import datetime
from typing import Any, Optional


class InMemoryConversationStore:
    """Small in-process conversation store used by the API prototype."""

    def __init__(self) -> None:
        self._conversations: dict[str, dict[str, Any]] = {}
        self._messages: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)

    def create_conversation(self, conversation_id: str, title: Optional[str] = None) -> None:
        self._conversations.setdefault(
            conversation_id,
            {
                "conversation_id": conversation_id,
                "title": title,
                "created_at": datetime.now().isoformat(),
            },
        )

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        self.create_conversation(conversation_id)
        self._messages[conversation_id].append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def get_messages(self, conversation_id: str) -> list[dict[str, Any]]:
        return list(self._messages.get(conversation_id, []))


memory = InMemoryConversationStore()
