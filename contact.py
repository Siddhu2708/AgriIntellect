import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
from utils import translate_text, load_config

config = load_config()

def send_email(form_data):
    # Retrieve credentials from config
    sender_email = form_data["email"]
    app_password = config.get("EMAIL_APP_PASSWORD", "")

    # Receiver email from config
    receiver_email = config.get("RECEIVER_EMAIL", "hireom07@gmail.com")

    # Set up the MIME message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"Contact Form Message from {form_data['name']}"

    # Email body content
    body = f"""
    You have received a new message from your contact form:

    Name: {form_data['name']}
    Email: {form_data['email']}
    Address: {form_data['address']}
    Phone: {form_data['phone']}

    Message:
    {form_data['message']}
    """

    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail's SMTP server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, app_password)  # Login with App Password
            server.sendmail(sender_email, receiver_email, message.as_string())
            st.success("Your message has been sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def Contact(sarvam_client, language):
    # Title for the Contact Us page
    st.title(translate_text(sarvam_client, "📞 Contact Us", language))
    st.write(translate_text(sarvam_client, "For any inquiries, reach out to us through the following contact details.", language))

    # Initialize session state for the form fields
    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "name": "",
            "email": "",
            "address": "",
            "phone": "",
            "message": ""
        }

    # Contact Form Inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.form_data["name"] = st.text_input(
            f"**{translate_text(sarvam_client, 'Your Name', language)}**",
            placeholder=translate_text(sarvam_client, "Enter your name", language),
            value=st.session_state.form_data["name"]
        )
        st.session_state.form_data["email"] = st.text_input(
            f"**{translate_text(sarvam_client, 'Your Email', language)}**",
            placeholder=translate_text(sarvam_client, "Enter your email", language),
            value=st.session_state.form_data["email"]
        )

    with col2:
        st.session_state.form_data["address"] = st.text_input(
            f"**{translate_text(sarvam_client, 'Your Address', language)}**",
            placeholder=translate_text(sarvam_client, "Enter your address", language),
            value=st.session_state.form_data["address"]
        )
        st.session_state.form_data["phone"] = st.text_input(
            f"**{translate_text(sarvam_client, 'Your Phone', language)}**",
            placeholder=translate_text(sarvam_client, "Enter your phone number", language),
            value=st.session_state.form_data["phone"]
        )

    with col3:
        st.session_state.form_data["message"] = st.text_area(
            f"**{translate_text(sarvam_client, 'Your Message', language)}**",
            placeholder=translate_text(sarvam_client, "Type your message here", language),
            value=st.session_state.form_data["message"]
        )

    # Submit Button
    if st.button(translate_text(sarvam_client, "SEND MESSAGE", language)):
        # Validation for mandatory fields
        if not st.session_state.form_data["name"] or not st.session_state.form_data["email"] or not \
        st.session_state.form_data["message"]:
            st.error(translate_text(sarvam_client, "Please fill out all required fields (Name, Email, and Message).", language))
        else:
            # Send the email
            send_email(st.session_state.form_data)

            # Reset all fields
            st.session_state.form_data = {
                "name": "",
                "email": "",
                "address": "",
                "phone": "",
                "message": ""
            }

        # 🌟 Expertise Team Section
    st.markdown ( "---" )
    st.subheader ( translate_text(sarvam_client, "🌟 Meet Our Experts", language) )
    st.write (
        translate_text(sarvam_client, "Our team of experts specializes in All Plant leaf disease detection. Feel free to reach out to them directly.", language) )

    experts = [
            {"name" : "Dr. Amit Kumar", "image" : "image/team-1.jpg", "phone" : "+91 98765 43210"},
            {"name" : "Dr. Neha Sharma", "image" : "image/team-5.jpg", "phone" : "+91 98234 56789"},
            {"name" : "Dr. Rajesh Verma", "image" : "image/team-4.jpg", "phone" : "+91 98712 34567"}
        ]

    col1, col2, col3 = st.columns ( 3 )

    for idx, expert in enumerate ( experts ) :
        with [col1, col2, col3][idx] :
            st.image ( expert["image"], width=200 )
            st.write ( f"**{translate_text(sarvam_client, expert['name'], language)}**" )
            st.write ( f"📞 {expert['phone']}" )

# Additional Information Section
    st.markdown("---")
    st.write(translate_text(sarvam_client, "For urgent inquiries, you can reach us through the following channels:", language))
    st.write(f"📞 **{translate_text(sarvam_client, 'Phone:', language)}** +1 (800) 123-4567")
    st.write(f"📧 **{translate_text(sarvam_client, 'Email:', language)}** support@agriintellect.com")
    st.write(f"🌐 **{translate_text(sarvam_client, 'Website:', language)}** [www.agriintellect.com](http://www.agriintellect.com)")
    st.write(f"📱 **{translate_text(sarvam_client, 'Instagram:', language)}** [@agriintellect](https://www.instagram.com/agriintellect)")
    st.write(f"🐦 **{translate_text(sarvam_client, 'Twitter:', language)}** [@agriintellect](https://www.twitter.com/agriintellect)")
    st.markdown("---")

# Run the contact function when the script is executed
if __name__ == "__main__":
    Contact(None, "English")
