from django.core.mail import send_mail

def send_approval_email(user, book):
    send_mail(
        'Livro Aprovado!',
        f'Seu livro "{book.title}" foi aprovado pelo administrador!',
        'no-reply@biblioteca.com',
        [user.email],
        fail_silently=False,
    )

def send_rejection_email(user, book, reason):
    send_mail(
        'Livro Rejeitado',
        f'Seu livro "{book.title}" foi rejeitado pelo administrador. Motivo: {reason}',
        'no-reply@biblioteca.com',
        [user.email],
        fail_silently=False,
    )
