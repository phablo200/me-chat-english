from fastapi import APIRouter, HTTPException, status

from history.schemas import (
    AppendMessageRequest,
    AppendMessageResponse,
    DeleteConversationResponse,
    StartConversationRequest,
    StartConversationResponse,
)
from history.services import (
    ConversationNotFoundError,
    InvalidMessageRoleError,
    append_message,
    delete_conversation,
    start_conversation,
)

router = APIRouter(prefix="/history", tags=["history"])


@router.post(
    "/conversations",
    response_model=StartConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_conversation_route(
    payload: StartConversationRequest,
) -> StartConversationResponse:
    try:
        response = await start_conversation(
            user_id=payload.user_id,
            title=payload.title,
            role=payload.initial_message.role,
            content=payload.initial_message.content,
        )
    except InvalidMessageRoleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return StartConversationResponse(**response)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=AppendMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def append_message_route(
    conversation_id: str,
    payload: AppendMessageRequest,
) -> AppendMessageResponse:
    try:
        response = await append_message(
            conversation_id=conversation_id,
            role=payload.role,
            content=payload.content,
        )
    except InvalidMessageRoleError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return AppendMessageResponse(**response)


@router.delete(
    "/conversations/{conversation_id}",
    response_model=DeleteConversationResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_conversation_route(conversation_id: str) -> DeleteConversationResponse:
    try:
        response = await delete_conversation(conversation_id=conversation_id)
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return DeleteConversationResponse(**response)
