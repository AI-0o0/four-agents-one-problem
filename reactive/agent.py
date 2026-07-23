from tools.travel_status_tools import (
    get_flight_status,
    get_delay_duration,
    check_alternative_transport,
)

from tools.finance_and_decision_tools import (
    CheckRefundEligibility,
    CalculateRefundAmount,
    ProcessRefund,
    IssueTravelVoucher,
)

from tools.escalation_tools import (
    escalate_to_human,
)


def run_agent():

    print("Reactive Travel Support Agent")

    flight_id = input("Flight ID: ").strip().upper()
    booking_id = input("Booking ID: ").strip().upper()
    destination = input("Destination Airport Code: ").strip().upper()

    # Rule 1: Flight Cancelled
    if get_flight_status.invoke(flight_id) == "Cancelled":

        alternatives = check_alternative_transport.invoke(destination)

        if alternatives:
            print("Alternative transport found:")
            print(alternatives)

        else:
            if CheckRefundEligibility.invoke(booking_id):

                refund = CalculateRefundAmount.invoke(booking_id)
                ProcessRefund.invoke(booking_id)

                print(f"Refund of ${refund} processed.")

            else:
                escalate_to_human.invoke(booking_id)
                print("Case escalated.")

        return

    # Rule 2: Delay > 6 hours
    delay = get_delay_duration.invoke(flight_id)

    if delay > 360:
        IssueTravelVoucher.invoke(booking_id)
        print("Hotel voucher issued.")
        return

    # Rule 3: Delay <= 2 hours
    if delay <= 120:
        print("Customer notified to wait for the flight.")
        return

    # Rule 4: Otherwise
    escalate_to_human.invoke(booking_id)
    print("Case escalated to human support.")


if __name__ == "__main__":
    run_agent()
