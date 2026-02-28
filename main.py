import streamlit as st
from datetime import date

from itinerary_service import generate_itinerary

# Streamlit UI
st.set_page_config(page_title="Tour Planner", layout="wide")

st.title("🌍 AI Tour Planning Itinerary Generator")
st.write("Plan your perfect trip with AI")

# User Inputs
destination = st.text_input("Enter Destination")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date", date.today())

with col2:
    end_date = st.date_input("End Date", date.today())

places = st.text_area("Places you want to visit (comma separated)")

food = st.text_area("Food preferences (street food, veg, non-veg, cafes, etc)")

activities = st.text_area("Activities (adventure, sightseeing, shopping, etc)")

budget = st.number_input("Estimated Budget (in USD or INR)", min_value=0)

generate_button = st.button("Generate Itinerary")


# Generate output
if generate_button:

    if destination == "":
        st.error("Please enter destination")
    else:

        with st.spinner("Generating itinerary..."):

            itinerary = generate_itinerary(
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                places=places,
                food=food,
                activities=activities,
                budget=budget,
            )

            # Try to extract a clearly formatted total estimated cost line
            total_cost_line = None
            lines = itinerary.splitlines()
            for line in lines:
                if line.strip().lower().startswith("total estimated cost:"):
                    total_cost_line = line.strip()
                    break

            # Remove the total cost line from the main body (we'll show it separately)
            if total_cost_line:
                body_lines = [l for l in lines if l.strip() != total_cost_line]
                itinerary_body = "\n".join(body_lines).strip()
            else:
                itinerary_body = itinerary

            st.success("Itinerary Generated Successfully!")

            st.subheader("📅 Your Travel Plan")

            st.markdown(itinerary_body)

            if total_cost_line:
                st.markdown("---")
                st.subheader("💰 Total Estimated Trip Cost")
                st.markdown(f"**{total_cost_line}**")

            st.download_button(
                label="Download Itinerary",
                data=itinerary,
                file_name="itinerary.txt",
                mime="text/plain"
            )
            