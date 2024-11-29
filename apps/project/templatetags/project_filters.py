from django import template

register = template.Library()


@register.filter
def total_projects(user):
    lead_count = 1 if user.project_lead.exists() else 0
    member_count = user.project_member.count()
    return lead_count + member_count
