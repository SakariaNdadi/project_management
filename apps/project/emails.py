from django.core.mail import send_mail


def project_invitation_email(project, email, role, invitation_link):
    """
    Sends an invitation email to the provided address.
    """
    subject = f"Invitation to join the project '{project.name}'"
    message = (
        f"You have been invited to join the project '{project.name}' as a {role}.\n\n"
        f"Click the link below to accept the invitation:\n{invitation_link}"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email="no-reply@example.com",
        recipient_list=[email],
    )
