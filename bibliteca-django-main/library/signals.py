
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Book

@receiver(post_save, sender=Book)
def send_book_notification(sender, instance, created, **kwargs):
    """Envia notificações baseadas no status do livro para todos os usuários."""
    if created:
        # Notifica todos os usuários sobre o novo livro adicionado
        users = User.objects.all()
        notify.send(
            instance.added_by,
            recipient_list=users,
            verb='Novo livro adicionado.',
            description=f'O livro "{instance.title}" foi adicionado e está aguardando revisão.'
        )
    elif instance.status == 'approved':
        # Notifica todos os usuários que o livro foi aprovado
        users = User.objects.all()
        notify.send(
            instance.added_by,
            recipient_list=users,
            verb='Livro aprovado.',
            description=f'O livro "{instance.title}" foi aprovado!'
        )
    elif instance.status == 'rejected':
        # Notifica todos os usuários que o livro foi rejeitado
        users = User.objects.all()
        notify.send(
            instance.added_by,
            recipient_list=users,
            verb='Livro rejeitado.',
            description=f'O livro "{instance.title}" foi rejeitado. Motivo: {instance.rejection_reason}'
        )