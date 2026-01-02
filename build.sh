#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create initial documents
python manage.py shell << EOF
from members.models import Document

# Check if documents already exist
if not Document.objects.exists():
    Document.objects.create(
        title="Liability Waiver and Release of Claims",
        content="""DOUBLE C RANCH LLC
WAIVER AND RELEASE OF LIABILITY, ASSUMPTION OF RISK AND INDEMNITY AGREEMENT

I hereby acknowledge that horseback riding and related equestrian activities involve inherent risks, including but not limited to the risk of serious injury or death. I understand that horses are unpredictable animals and that accidents can occur.

By signing this document, I voluntarily assume all risks associated with participation in horseback riding activities at Double C Ranch LLC. I agree to release, waive, discharge, and covenant not to sue Double C Ranch LLC, its owners, employees, instructors, and agents from any and all liability, claims, demands, actions, and causes of action whatsoever arising out of or related to any loss, damage, or injury that may be sustained by me while participating in such activities.

I understand that this release discharges Double C Ranch LLC from any liability or claim that I may have against them with respect to any bodily injury, personal injury, illness, death, or property damage that may result from my participation in horseback riding activities.

I have read this waiver of liability, assumption of risk, and indemnity agreement, fully understand its terms, and understand that I am giving up substantial rights, including my right to sue. I acknowledge that I am signing the agreement freely and voluntarily.""",
        is_required=True
    )
    
    Document.objects.create(
        title="Riding Lesson Agreement",
        content="""DOUBLE C RANCH LLC - RIDING LESSON AGREEMENT

This agreement is entered into between Double C Ranch LLC and the undersigned participant/guardian.

TERMS AND CONDITIONS:
1. Lessons are scheduled by appointment and must be confirmed 24 hours in advance.
2. Cancellations must be made at least 24 hours before the scheduled lesson time.
3. Late cancellations (less than 24 hours notice) will result in forfeiture of the lesson fee.
4. Participants must arrive 15 minutes before their scheduled lesson time.
5. Appropriate riding attire is required: long pants, closed-toe shoes with a heel, and ASTM-approved helmet (provided by ranch if needed).
6. Participants must follow all instructions given by ranch staff and instructors.
7. Participants under 18 must have a parent or guardian present during lessons.

PAYMENT:
- Lesson fees are due at the time of booking.
- Package deals and memberships are non-refundable.
- Returned checks will incur a $35 fee.

HEALTH AND SAFETY:
- Participants must disclose any medical conditions, physical limitations, or medications that may affect their ability to ride safely.
- Participants must not be under the influence of alcohol or drugs.
- The ranch reserves the right to refuse service to anyone deemed unfit to ride.

By signing this agreement, I acknowledge that I have read, understood, and agree to abide by all terms and conditions set forth above.""",
        is_required=True
    )
    
    print("✓ Initial documents created")
else:
    print("✓ Documents already exist")
EOF
