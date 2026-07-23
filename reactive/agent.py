from shared.data import FLIGHTS
from tools.flight_tools import (
    check_alternative_transport,
    get_delay_duration,
)
from tools.booking_tools import (
    check_refund_eligibility,
    calculate_refund_amount,
    process_refund,
)
from tools.customer_tools import notify_customer
from tools.escalation_tools import (
    issue_travel_voucher,
    escalate_to_human,
)


def run_agent():

    print("Reactive Travel Support Agent")

    flight_id = input("Flight ID: ").strip().upper()
    booking_id = input("Booking ID: ").strip().upper()

    if flight_id not in FLIGHTS:
        print("Flight not found.")
        return

    flight = FLIGHTS[flight_id]

    # Rule 1
    if flight["status"] == "Cancelled":

        alternatives = check_alternative_transport(
            flight["arrival_airport"]
        )

        if alternatives:
            print("Alternative transport found:")
            print(alternatives)

        else:
            if check_refund_eligibility(booking_id):
                refund = calculate_refund_amount(booking_id)
                process_refund(booking_id)

                print(f"Refund of ${refund} processed.")

            else:
                escalate_to_human(booking_id)
                print("Case escalated.")

        return

    # Rule 2
    delay = get_delay_duration(flight_id)

    if delay > 360:
        issue_travel_voucher(booking_id)
        print("Hotel voucher issued.")
        return

    # Rule 3
    if delay <= 120:
        notify_customer(
            booking_id,
            "Please wait. Your flight will depart shortly."
        )
        print("Customer notified.")
        return

    # Rule 4
    # else -> escalate_to_human
    escalate_to_human(booking_id)
    print("Case escalated to human support.")


if __name__ == "__main__":
    run_agent()
