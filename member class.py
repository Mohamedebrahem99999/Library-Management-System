import json

users = []
next_id = 1
USERS_FILE = "library_users.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


def save_users_to_json():
    data = {
        "users": users,
        "next_id": next_id
    }

    with open(USERS_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Users saved successfully.")


def load_users_from_json():
    global users, next_id

    try:
        with open(USERS_FILE, "r") as file:
            data = json.load(file)

        users.clear()
        users.extend(data.get("users", []))
        next_id = data.get("next_id", 1)

        print("Users loaded successfully.")

    except FileNotFoundError:
        users = []
        next_id = 1
        print("No JSON file found. Starting with empty users.")


def register():
    global next_id

    name = input("Please enter your name: ").strip()
    password = input("Please enter your password: ").strip()

    while True:
        phone = input("Please enter your phone number: ").strip()

        if phone.isdigit() and len(phone) == 11:
            break
        else:
            print("Invalid phone number. Please enter exactly 11 digits.")

    email = input("Please enter your email: ").strip()
    gender = input("Please enter your gender: ").strip()

    for user in users:
        if user["phone"] == phone:
            print("Phone number already exists.")
            return

        if user["email"] == email:
            print("Email already exists.")
            return

    while True:
        age_input = input("Please enter your age: ").strip()

        if age_input.isdigit():
            age = int(age_input)
            break
        else:
            print("Invalid age. Please enter a number.")

    city = input("Please enter your city: ").strip()

    new_user = {
        "id": str(next_id),
        "name": name,
        "password": password,
        "phone": phone,
        "email": email,
        "gender": gender,
        "age": age,
        "city": city,
        "failed_login": False
    }

    users.append(new_user)

    print(f"Sign up successful. Your ID is {next_id}")

    next_id += 1


def find_user_by_id(user_id):
    for user in users:
        if user["id"] == str(user_id):
            return user

    return None


def login():
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        id_input = input("Please enter your ID: ").strip()

        if not id_input.isdigit():
            print("Invalid ID format. Please enter a number.")
            attempts += 1
            print(f"Attempts remaining: {max_attempts - attempts}")
            continue

        password = input("Please enter your password: ").strip()

        user = find_user_by_id(id_input)

        if user is not None and user["password"] == password:
            user["active"] = True
            print(f"Login successful. Welcome, {user['name']}!")
            return user

        if user is not None:
            user["failed_login"] = True

        attempts += 1

        print("Invalid ID or password.")

        if attempts < max_attempts:
            print(f"Attempts remaining: {max_attempts - attempts}")

    print("Too many failed attempts. Returning to home page.")
    return None


def admin_login():
    username = input("Please enter admin username: ").strip()
    password = input("Please enter admin password: ").strip()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful.")
        admin_menu()
    else:
        print("Invalid admin username or password.")
        print("Returning to home page.")


def show_all_users():
    if len(users) == 0:
        print("No users found.")
        return

    print("\n========== ALL USERS ==========")

    for user in users:
        print(f"ID: {user['id']}")
        print(f"Name: {user['name']}")
        print(f"Phone: {user['phone']}")
        print(f"Email: {user['email']}")
        print(f"Gender: {user['gender']}")
        print(f"Age: {user['age']}")
        print(f"City: {user['city']}")
        print(f"Failed Login: {user['failed_login']}")
        print("------------------------------")


def admin_menu():
    while True:
        print("\n******** ADMIN MENU ********")
        print("1. View all users")
        print("2. Save users to JSON")
        print("3. Load users from JSON")
        print("4. Back to home page")

        choice = input("> ").strip()

        if choice == "1":
            show_all_users()

        elif choice == "2":
            save_users_to_json()

        elif choice == "3":
            load_users_from_json()

        elif choice == "4":
            print("Returning to home page.")
            break

        else:
            print("Invalid option.")


def user_menu(user):
    while True:
        print("\n******** USER MENU ********")
        print("1. Show profile")
        print("2. Logout")

        choice = input("> ").strip()

        if choice == "1":
            print(f"ID: {user['id']}")
            print(f"Name: {user['name']}")
            print(f"Email: {user['email']}")
            print(f"Phone: {user['phone']}")

        elif choice == "2":
            user["active"] = False
            print("Logged out successfully.")
            print("Returning to home page.")
            break

        else:
            print("Invalid option.")


def home_page():
    while True:
        print(
            "\n************************************* "
            "SIC SMART LIBRARY SYSTEM "
            "*************************************"
        )

        print("If you already have an account, enter [1] login")
        print("If you do not have an account, enter [2] register")
        print("For admin access, enter [3] admin")
        print("To close the system, enter [4] exit\n")

        choice = input("> ").strip().lower()

        if choice == "login" or choice == "1":
            user = login()

            if user is not None:
                user_menu(user)

        elif choice == "register" or choice == "2":
            register()
            print("Returning to home page.")

        elif choice == "admin" or choice == "3":
            admin_login()

        elif choice == "exit" or choice == "4":
            save_users_to_json()
            print(
                "Thank you for using SIC Smart Library System. "
                "Goodbye!"
            )
            break

        else:
            print(
                "Invalid option. Please enter "
                "[1] login, [2] register, [3] admin or [4] exit."
            )


if __name__ == "__main__":
    load_users_from_json()
    home_page()
