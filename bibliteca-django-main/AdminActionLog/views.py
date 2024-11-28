from django.shortcuts import render
from .models import AdminActionLog
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def action_log_view(request):
    logs = AdminActionLog.objects.all().order_by('-created_at')
    return render(request, 'AdminActionLog/action_log.html', {'logs': logs})

@staff_member_required
def approve_book(request, pk):
    book = get_object_or_404(Book, pk=pk, status='pending')
    book.status = 'approved'
    book.save()

    # Enviar e-mail de aprovação
    send_approval_email(book.added_by, book)

    # Registrar no log de auditoria
    AdminActionLog.objects.create(admin_user=request.user, book=book, action='accept')

    messages.success(request, f"O livro '{book.title}' foi aprovado.")
    return redirect('dashboard')


@staff_member_required
def reject_book(request, pk):
    book = get_object_or_404(Book, pk=pk, status='pending')
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        book.status = 'rejected'
        book.rejection_reason = reason
        book.save()

        # Enviar e-mail de rejeição
        send_rejection_email(book.added_by, book, reason)

        # Registrar no log de auditoria
        AdminActionLog.objects.create(admin_user=request.user, book=book, action='reject', reason=reason)

        messages.success(request, f"O livro '{book.title}' foi rejeitado.")
        return redirect('dashboard')

    return render(request, 'library/reject_book.html', {'book': book})
