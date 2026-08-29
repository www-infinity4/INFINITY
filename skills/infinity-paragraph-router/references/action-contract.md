# Paragraph Action Contract

Machine-readable actions should contain:

- stable action ID;
- source block, conversation reference, and position;
- integrity mode: exact private reference, exact approved text, or approved summary;
- action name;
- human or robot actor;
- named destination when routing;
- proposed color route;
- authorization and privacy-review state;
- proposed, approved, executing, complete, blocked, or rejected status;
- completion receipt.

A completion receipt records that the source was preserved, the actual destination, any created conversation/file/issue reference, an optional commit SHA, and completion time.

Routing actions that leave the current conversation require a destination, authorization check, and privacy review. A complete action requires a receipt. Folding and discussing locally do not change the source color unless the content itself enters a new operation.
