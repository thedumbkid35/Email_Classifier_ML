import sys
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def generate_spam_ham_data(num_samples=200):
    spam_templates = [
        "Congratulations! You've won a ${amount} gift card. Click {link} to claim your prize.",
        "Earn ${amount} per month from home! No experience required. Visit {link} now.",
        "You've been selected for a free {item}. Claim it fast at {link}.",
        "Limited time offer: Buy one {item}, get one free! Check it out at {link}.",
        "You're a lucky winner of our {type} lottery! Claim your prize today.",
        "Don't miss out on exclusive deals! Visit {link} for more details.",
        "Your account shows suspicious activity. Verify now at {link}.",
        "Please provide your OTP for the following",
        "New message from {sender}. Open it immediately at {link}.",
        "Act quickly! Your chance to win {item} ends soon.",
        "Work from home and earn ${amount} quickly! Details at {link}.",
        "Airtel has launched its new premium offer!",
        "URGENT: Your account has been suspended. Click here immediately to restore access.",
        "You won’t believe this—$10,000 deposited straight to my account with no work!",
        "Your antivirus has expired. Renew now to protect your computer!"
    ]

    ham_serious = [
        "Please find attached the project report.",
        "Reminder: Submit your tax documents.",
        "Meeting confirmed at 10 AM tomorrow.",
        "Urgent: Action required on your invoice.",
        "Security alert: Suspicious login detected.",
        "Hi {name}, I hope this email finds you well. Let's catch up soon.",
        "Dear {name}, can we schedule a call to discuss the {topic} project?",
        "Hi {name}, just wanted to confirm our meeting on {date}. Let me know if the time still works.",
        "Your account has been credited with $500.",
        "Please come to class on time from now on",
         "Your order has shipped! Track it here.",
         "You have a new message from Bob. Check it out now!",
         "Your ride is on the way! Estimated arrival: 5 minutes.",
        "Please find the attached document related to our {topic} discussion.",
        "Thank you for your response, {name}. I appreciate your support.",
        "Hi {name}, looking forward to discussing project updates during our next meeting.",
        "Dear {name}, please share your thoughts on the attached proposal.",
        "Hi {name}, here's the update regarding the {topic} you requested.",
        "Congratulations baby! You're a dad now!",
        "Congratulations! You are pregnant!",
        "Don’t forget to submit your timesheet before 6 PM today.",
        
    ]

    ham_chill = [
        "You have a new friend request from Alice.",
        "Hey! Wanna grab coffee later?",
        "Hope you're having a chill weekend!",
        "Let's hang out soon.",
        "This meme made my day 😂",
        "Brunch tomorrow?",
        "Hey bro! What's up? How are you doing?",
        "I love you so much",
        "Come home by 9 pm",
        "New comment on your photo! Check it out now.",
        "Good morning {name}, hope you are having a productive day.",
        "Hello {name}, can you let me know your availability for a quick chat?",
        "Hey Bro, Up for a drink?",
        "Hi baby! Can we go have a drink?",
        "Hey, just checking in—did you get a chance to look at that job post I sent?",
        "Haha I just walked into the wrong conference room and sat for 10 mins before realizing 😅"
    ]

    def fill_template(template):
        return template.format(
            amount=random.randint(100, 1000),
            link="http://example.com",
            item=random.choice(["iPhone", "laptop", "gift box", "voucher"]),
            type=random.choice(["holiday", "cash", "tech"]),
            sender=random.choice(["admin", "support", "John"]),
            name=random.choice(["Alice", "Bob", "Charlie", "Dana"]),
            topic=random.choice(["sales", "budget", "design"]),
            date=random.choice(["Monday", "July 21st", "next week"])
        )

    spam = [fill_template(random.choice(spam_templates)) for _ in range(num_samples // 3)]
    ham_serious_filled = [random.choice(ham_serious) for _ in range(num_samples // 3)]
    ham_chill_filled = [random.choice(ham_chill) for _ in range(num_samples // 3)]

    texts = spam + ham_serious_filled + ham_chill_filled
    labels = ['spam'] * len(spam) + ['ham_serious'] * len(ham_serious_filled) + ['ham_chill'] * len(ham_chill_filled)

    return texts, labels


X_train, y_train = generate_spam_ham_data(600)
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
model = MultinomialNB()
model.fit(X_train_vec, y_train)


input_data = sys.stdin.read()
try:
    input_json = json.loads(input_data)
    emails = input_json.get("emails", [])
except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON input"}))
    sys.exit(1)


X_test_vec = vectorizer.transform(emails)
predictions = model.predict(X_test_vec)


output = {
    "ham_serious": [email for email, label in zip(emails, predictions) if label == 'ham_serious'],
    "ham_chill": [email for email, label in zip(emails, predictions) if label == 'ham_chill'],
    "spam": [email for email, label in zip(emails, predictions) if label == 'spam']
}

print(json.dumps(output))
