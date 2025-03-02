`can_view`: Allows users to view books.
- `can_create`: Allows users to create books.
- `can_edit`: Allows users to edit books.
- `can_delete`: Allows users to delete books.

## Groups
The following groups are created and assigned permissions:
- **Viewers**: Can view books.
- **Editors**: Can view, create, and edit books.
- **Admins**: Can view, create, edit, and delete books.

## Views
Views are protected using the `@permission_required` decorator to enforce these permissions.
Deliverables
models.py: Updated with custom permissions for the Book model.

views.py: Updated to include permission checks in relevant views.




