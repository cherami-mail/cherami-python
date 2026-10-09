# Generated from openapi.json by bun scripts/generate.mts. Do not edit.
from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal, overload
import httpx
from . import models
from ._transport import ApiResponse, DEFAULT_TIMEOUT, Timeout
from ._client import SyncClient, AsyncClient
from ._routes import ROUTES

class Cherami(SyncClient):
    def list_inboxes(self, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListInboxesResult]:
        """List inboxes. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_inboxes"], {}, timeout=timeout)

    def create_inbox(self, params: models.CreateInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.CreateInboxResult]:
        """Create an inbox. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["create_inbox"], params, timeout=timeout)

    def get_inbox(self, params: models.GetInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetInboxResult]:
        """Read an inbox. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_inbox"], params, timeout=timeout)

    def update_inbox(self, params: models.UpdateInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateInboxResult]:
        """Edit inbox names. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["update_inbox"], params, timeout=timeout)

    def delete_inbox(self, params: models.DeleteInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteInboxResult]:
        """Delete an inbox. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["delete_inbox"], params, timeout=timeout)

    def get_sending_policy(self, params: models.GetSendingPolicyParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetSendingPolicyResult]:
        """Inspect sending rules. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_sending_policy"], params, timeout=timeout)

    def get_receiving_policy(self, params: models.GetReceivingPolicyParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetReceivingPolicyResult]:
        """Inspect receiving rules. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_receiving_policy"], params, timeout=timeout)

    def list_messages(self, params: models.ListMessagesParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListMessagesResult]:
        """List received messages. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_messages"], params, timeout=timeout)

    def count_messages(self, params: models.CountMessagesParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.CountMessagesResult]:
        """Count received messages. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["count_messages"], params, timeout=timeout)

    def get_message(self, params: models.GetMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetMessageResult]:
        """Read a received message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_message"], params, timeout=timeout)

    def delete_message(self, params: models.DeleteMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteMessageResult]:
        """Delete a received message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["delete_message"], params, timeout=timeout)

    def update_message_labels(self, params: models.UpdateMessageLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateMessageLabelsResult]:
        """Label a received message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["update_message_labels"], params, timeout=timeout)

    def download_raw_message(self, params: models.DownloadRawMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[httpx.Response]:
        """Download raw MIME. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["download_raw_message"], params, timeout=timeout)

    def download_attachment(self, params: models.DownloadAttachmentParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[httpx.Response]:
        """Download a received attachment. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["download_attachment"], params, timeout=timeout)

    def delete_sent_message(self, params: models.DeleteSentMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteSentMessageResult]:
        """Delete a sent copy. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["delete_sent_message"], params, timeout=timeout)

    def update_sent_message_labels(self, params: models.UpdateSentMessageLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateSentMessageLabelsResult]:
        """Label a sent copy. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["update_sent_message_labels"], params, timeout=timeout)

    def get_sent_message(self, params: models.GetSentMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetSentMessageResult]:
        """Read a sent message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_sent_message"], params, timeout=timeout)

    def bulk_update_message_labels(self, params: models.BulkUpdateMessageLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.BulkUpdateMessageLabelsResult]:
        """Label several received messages. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["bulk_update_message_labels"], params, timeout=timeout)

    def bulk_update_sent_labels(self, params: models.BulkUpdateSentLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.BulkUpdateSentLabelsResult]:
        """Label several sent copies. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["bulk_update_sent_labels"], params, timeout=timeout)

    def list_labels(self, params: models.ListLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListLabelsResult]:
        """Discover labels. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_labels"], params, timeout=timeout)

    def send_message(self, params: models.SendMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.SendMessageResult]:
        """Send a message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["send_message"], params, timeout=timeout)

    def list_sent_messages(self, params: models.ListSentMessagesParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListSentMessagesResult]:
        """List sent messages. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_sent_messages"], params, timeout=timeout)

    def reply_message(self, params: models.ReplyMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ReplyMessageResult]:
        """Reply to a message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["reply_message"], params, timeout=timeout)

    def reply_all_message(self, params: models.ReplyAllMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ReplyAllMessageResult]:
        """Reply to all. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["reply_all_message"], params, timeout=timeout)

    def forward_message(self, params: models.ForwardMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ForwardMessageResult]:
        """Forward a message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["forward_message"], params, timeout=timeout)

    def get_outbound_quota(self, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetOutboundQuotaResult]:
        """Read sending allowance. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_outbound_quota"], {}, timeout=timeout)

    def create_draft(self, params: models.CreateDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.CreateDraftResult]:
        """Create a draft. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["create_draft"], params, timeout=timeout)

    def list_drafts(self, params: models.ListDraftsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListDraftsResult]:
        """List drafts. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_drafts"], params, timeout=timeout)

    def get_draft(self, params: models.GetDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetDraftResult]:
        """Retrieve a draft. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_draft"], params, timeout=timeout)

    def update_draft(self, params: models.UpdateDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateDraftResult]:
        """Edit a draft. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["update_draft"], params, timeout=timeout)

    def delete_draft(self, params: models.DeleteDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteDraftResult]:
        """Delete a draft. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["delete_draft"], params, timeout=timeout)

    def send_draft(self, params: models.SendDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.SendDraftResult]:
        """Send a draft. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["send_draft"], params, timeout=timeout)

    def list_threads(self, params: models.ListThreadsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListThreadsResult]:
        """List conversations. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_threads"], params, timeout=timeout)

    def get_thread(self, params: models.GetThreadParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetThreadResult]:
        """Read a conversation. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["get_thread"], params, timeout=timeout)

    def update_thread_labels(self, params: models.UpdateThreadLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateThreadLabelsResult]:
        """Label a conversation. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["update_thread_labels"], params, timeout=timeout)

    def delete_thread(self, params: models.DeleteThreadParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteThreadResult]:
        """Delete a conversation. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["delete_thread"], params, timeout=timeout)

    def list_trash(self, params: models.ListTrashParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListTrashResult]:
        """List Trash. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["list_trash"], params, timeout=timeout)

    def restore_message(self, params: models.RestoreMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.RestoreMessageResult]:
        """Restore a received message. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["restore_message"], params, timeout=timeout)

    def restore_sent_message(self, params: models.RestoreSentMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.RestoreSentMessageResult]:
        """Restore a sent copy. See the HTTP reference for state/recovery semantics."""
        return self._request(ROUTES["restore_sent_message"], params, timeout=timeout)

    @overload
    def pages(self, operation: Literal["list_messages"], params: models.ListMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.ListMessagesResult]]: ...

    @overload
    def pages(self, operation: Literal["list_labels"], params: models.ListLabelsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.ListLabelsResult]]: ...

    @overload
    def pages(self, operation: Literal["list_sent_messages"], params: models.ListSentMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.ListSentMessagesResult]]: ...

    @overload
    def pages(self, operation: Literal["list_drafts"], params: models.ListDraftsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.ListDraftsResult]]: ...

    @overload
    def pages(self, operation: Literal["list_threads"], params: models.ListThreadsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.ListThreadsResult]]: ...

    @overload
    def pages(self, operation: Literal["get_thread"], params: models.GetThreadParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.GetThreadResult]]: ...

    @overload
    def pages(self, operation: Literal["list_trash"], params: models.ListTrashParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[models.ListTrashResult]]: ...

    def pages(self, operation: str, params: Any, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[ApiResponse[Any]]:
        return self._pages(operation, params, max_pages=max_pages, timeout=timeout)

    @overload
    def iterate(self, operation: Literal["list_messages"], params: models.ListMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.ListMessagesItem]: ...

    @overload
    def iterate(self, operation: Literal["list_labels"], params: models.ListLabelsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.ListLabelsItem]: ...

    @overload
    def iterate(self, operation: Literal["list_sent_messages"], params: models.ListSentMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.ListSentMessagesItem]: ...

    @overload
    def iterate(self, operation: Literal["list_drafts"], params: models.ListDraftsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.ListDraftsItem]: ...

    @overload
    def iterate(self, operation: Literal["list_threads"], params: models.ListThreadsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.ListThreadsItem]: ...

    @overload
    def iterate(self, operation: Literal["get_thread"], params: models.GetThreadParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.GetThreadItem]: ...

    @overload
    def iterate(self, operation: Literal["list_trash"], params: models.ListTrashParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[models.ListTrashItem]: ...

    def iterate(self, operation: str, params: Any, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> Iterator[Any]:
        return self._iterate(operation, params, max_pages=max_pages, timeout=timeout)


class AsyncCherami(AsyncClient):
    async def list_inboxes(self, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListInboxesResult]:
        """List inboxes. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_inboxes"], {}, timeout=timeout)

    async def create_inbox(self, params: models.CreateInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.CreateInboxResult]:
        """Create an inbox. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["create_inbox"], params, timeout=timeout)

    async def get_inbox(self, params: models.GetInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetInboxResult]:
        """Read an inbox. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_inbox"], params, timeout=timeout)

    async def update_inbox(self, params: models.UpdateInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateInboxResult]:
        """Edit inbox names. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["update_inbox"], params, timeout=timeout)

    async def delete_inbox(self, params: models.DeleteInboxParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteInboxResult]:
        """Delete an inbox. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["delete_inbox"], params, timeout=timeout)

    async def get_sending_policy(self, params: models.GetSendingPolicyParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetSendingPolicyResult]:
        """Inspect sending rules. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_sending_policy"], params, timeout=timeout)

    async def get_receiving_policy(self, params: models.GetReceivingPolicyParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetReceivingPolicyResult]:
        """Inspect receiving rules. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_receiving_policy"], params, timeout=timeout)

    async def list_messages(self, params: models.ListMessagesParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListMessagesResult]:
        """List received messages. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_messages"], params, timeout=timeout)

    async def count_messages(self, params: models.CountMessagesParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.CountMessagesResult]:
        """Count received messages. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["count_messages"], params, timeout=timeout)

    async def get_message(self, params: models.GetMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetMessageResult]:
        """Read a received message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_message"], params, timeout=timeout)

    async def delete_message(self, params: models.DeleteMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteMessageResult]:
        """Delete a received message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["delete_message"], params, timeout=timeout)

    async def update_message_labels(self, params: models.UpdateMessageLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateMessageLabelsResult]:
        """Label a received message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["update_message_labels"], params, timeout=timeout)

    async def download_raw_message(self, params: models.DownloadRawMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[httpx.Response]:
        """Download raw MIME. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["download_raw_message"], params, timeout=timeout)

    async def download_attachment(self, params: models.DownloadAttachmentParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[httpx.Response]:
        """Download a received attachment. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["download_attachment"], params, timeout=timeout)

    async def delete_sent_message(self, params: models.DeleteSentMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteSentMessageResult]:
        """Delete a sent copy. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["delete_sent_message"], params, timeout=timeout)

    async def update_sent_message_labels(self, params: models.UpdateSentMessageLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateSentMessageLabelsResult]:
        """Label a sent copy. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["update_sent_message_labels"], params, timeout=timeout)

    async def get_sent_message(self, params: models.GetSentMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetSentMessageResult]:
        """Read a sent message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_sent_message"], params, timeout=timeout)

    async def bulk_update_message_labels(self, params: models.BulkUpdateMessageLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.BulkUpdateMessageLabelsResult]:
        """Label several received messages. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["bulk_update_message_labels"], params, timeout=timeout)

    async def bulk_update_sent_labels(self, params: models.BulkUpdateSentLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.BulkUpdateSentLabelsResult]:
        """Label several sent copies. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["bulk_update_sent_labels"], params, timeout=timeout)

    async def list_labels(self, params: models.ListLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListLabelsResult]:
        """Discover labels. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_labels"], params, timeout=timeout)

    async def send_message(self, params: models.SendMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.SendMessageResult]:
        """Send a message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["send_message"], params, timeout=timeout)

    async def list_sent_messages(self, params: models.ListSentMessagesParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListSentMessagesResult]:
        """List sent messages. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_sent_messages"], params, timeout=timeout)

    async def reply_message(self, params: models.ReplyMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ReplyMessageResult]:
        """Reply to a message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["reply_message"], params, timeout=timeout)

    async def reply_all_message(self, params: models.ReplyAllMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ReplyAllMessageResult]:
        """Reply to all. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["reply_all_message"], params, timeout=timeout)

    async def forward_message(self, params: models.ForwardMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ForwardMessageResult]:
        """Forward a message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["forward_message"], params, timeout=timeout)

    async def get_outbound_quota(self, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetOutboundQuotaResult]:
        """Read sending allowance. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_outbound_quota"], {}, timeout=timeout)

    async def create_draft(self, params: models.CreateDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.CreateDraftResult]:
        """Create a draft. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["create_draft"], params, timeout=timeout)

    async def list_drafts(self, params: models.ListDraftsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListDraftsResult]:
        """List drafts. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_drafts"], params, timeout=timeout)

    async def get_draft(self, params: models.GetDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetDraftResult]:
        """Retrieve a draft. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_draft"], params, timeout=timeout)

    async def update_draft(self, params: models.UpdateDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateDraftResult]:
        """Edit a draft. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["update_draft"], params, timeout=timeout)

    async def delete_draft(self, params: models.DeleteDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteDraftResult]:
        """Delete a draft. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["delete_draft"], params, timeout=timeout)

    async def send_draft(self, params: models.SendDraftParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.SendDraftResult]:
        """Send a draft. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["send_draft"], params, timeout=timeout)

    async def list_threads(self, params: models.ListThreadsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListThreadsResult]:
        """List conversations. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_threads"], params, timeout=timeout)

    async def get_thread(self, params: models.GetThreadParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.GetThreadResult]:
        """Read a conversation. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["get_thread"], params, timeout=timeout)

    async def update_thread_labels(self, params: models.UpdateThreadLabelsParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.UpdateThreadLabelsResult]:
        """Label a conversation. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["update_thread_labels"], params, timeout=timeout)

    async def delete_thread(self, params: models.DeleteThreadParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.DeleteThreadResult]:
        """Delete a conversation. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["delete_thread"], params, timeout=timeout)

    async def list_trash(self, params: models.ListTrashParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.ListTrashResult]:
        """List Trash. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["list_trash"], params, timeout=timeout)

    async def restore_message(self, params: models.RestoreMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.RestoreMessageResult]:
        """Restore a received message. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["restore_message"], params, timeout=timeout)

    async def restore_sent_message(self, params: models.RestoreSentMessageParams, *, timeout: Timeout = DEFAULT_TIMEOUT) -> ApiResponse[models.RestoreSentMessageResult]:
        """Restore a sent copy. See the HTTP reference for state/recovery semantics."""
        return await self._request(ROUTES["restore_sent_message"], params, timeout=timeout)

    @overload
    def pages(self, operation: Literal["list_messages"], params: models.ListMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.ListMessagesResult]]: ...

    @overload
    def pages(self, operation: Literal["list_labels"], params: models.ListLabelsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.ListLabelsResult]]: ...

    @overload
    def pages(self, operation: Literal["list_sent_messages"], params: models.ListSentMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.ListSentMessagesResult]]: ...

    @overload
    def pages(self, operation: Literal["list_drafts"], params: models.ListDraftsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.ListDraftsResult]]: ...

    @overload
    def pages(self, operation: Literal["list_threads"], params: models.ListThreadsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.ListThreadsResult]]: ...

    @overload
    def pages(self, operation: Literal["get_thread"], params: models.GetThreadParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.GetThreadResult]]: ...

    @overload
    def pages(self, operation: Literal["list_trash"], params: models.ListTrashParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[models.ListTrashResult]]: ...

    def pages(self, operation: str, params: Any, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[ApiResponse[Any]]:
        return self._pages(operation, params, max_pages=max_pages, timeout=timeout)

    @overload
    def iterate(self, operation: Literal["list_messages"], params: models.ListMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.ListMessagesItem]: ...

    @overload
    def iterate(self, operation: Literal["list_labels"], params: models.ListLabelsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.ListLabelsItem]: ...

    @overload
    def iterate(self, operation: Literal["list_sent_messages"], params: models.ListSentMessagesParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.ListSentMessagesItem]: ...

    @overload
    def iterate(self, operation: Literal["list_drafts"], params: models.ListDraftsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.ListDraftsItem]: ...

    @overload
    def iterate(self, operation: Literal["list_threads"], params: models.ListThreadsParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.ListThreadsItem]: ...

    @overload
    def iterate(self, operation: Literal["get_thread"], params: models.GetThreadParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.GetThreadItem]: ...

    @overload
    def iterate(self, operation: Literal["list_trash"], params: models.ListTrashParams, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[models.ListTrashItem]: ...

    def iterate(self, operation: str, params: Any, *, max_pages: int | None = None, timeout: Timeout = DEFAULT_TIMEOUT) -> AsyncIterator[Any]:
        return self._iterate(operation, params, max_pages=max_pages, timeout=timeout)
