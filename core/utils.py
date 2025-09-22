from datetime import date
from decimal import Decimal


def compute_credit_score(customer):
    loans = customer.loans.filter(approved=True)

    # if sum of active loan amounts > approved_limit => 0
    active_loans = [l for l in loans if (l.end_date is None or l.end_date >= date.today())]
    sum_active = sum([l.loan_amount for l in active_loans], Decimal(0))
    if sum_active > customer.approved_limit:
        return 0

    # components
    total_loans = loans.count() or 1
    timely_emi_count = sum(getattr(l, 'emIs_paid_on_time', 0) for l in loans)
    total_emis_count = sum(getattr(l, 'total_emis', l.tenure_months) for l in loans) or 1
    timely_ratio = timely_emi_count / total_emis_count  # 0..1

    # number of loans penalty (more loans -> slight penalty)
    loan_count_penalty = max(0, min(20, (total_loans - 1) * 5))  # up to 20 points penalty

    # volume factor (how much of approved limit used by past loans)
    total_past_volume = sum(l.loan_amount for l in loans)
    volume_ratio = float(total_past_volume / Decimal(max(1, customer.approved_limit)))
    # clamp
    volume_score = max(0, 1 - volume_ratio)  # high volume => lower score

    # activity in current year
    current_year = date.today().year
    current_year_loans = [l for l in loans if (l.start_date and l.start_date.year == current_year)]
    activity_bonus = min(10, len(current_year_loans) * 5)  # reward recent good activity

    # Compose final score (weights)
    score = 100 * (0.6 * timely_ratio + 0.25 * volume_score + 0.15 * (1 - loan_count_penalty/20))
    score = score + activity_bonus - loan_count_penalty
    score = int(max(0, min(100, score)))
    return score