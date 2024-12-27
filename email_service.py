import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from config import EMAIL_CONFIG

class EmailService:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.sender_email = EMAIL_CONFIG['sender_email']
        self.sender_password = EMAIL_CONFIG['sender_password']

    def send_daily_report(self, report_data):
        """Send daily report email with assets information and graphs"""
        msg = MIMEMultipart()
        msg['Subject'] = f"Daily Asset Report - {report_data['date']}"
        msg['From'] = self.sender_email
        msg['To'] = EMAIL_CONFIG['recipient_email']

        # Create HTML content
        html_content = f"""
        <html>
            <body>
                <h2>Daily Asset Report - {report_data['date']}</h2>
                <table>
                    <tr>
                        <th>Asset</th>
                        <th>Price (USD)</th>
                        <th>24h Change</th>
                        <th>Graph</th>
                    </tr>
        """

        # Add asset information and graphs
        for asset in report_data['assets']:
            html_content += f"""
                <tr>
                    <td>{asset['name']}</td>
                    <td>${asset['price']:.2f}</td>
                    <td>{asset['daily_change']:.2f}%</td>
                    <td><img src="cid:{asset['name']}_graph"></td>
                </tr>
            """

            # Attach graph image
            with open(asset['graph_path'], 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', f'<{asset["name"]}_graph>')
                msg.attach(img)

        html_content += """
                </table>
            </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)