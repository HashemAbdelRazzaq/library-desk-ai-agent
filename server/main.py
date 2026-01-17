from server.agent import create_agent


def main():
    agent = create_agent()

    print("Library AI Assistant")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = agent.run(user_input)
        print("AI:", response)


if __name__ == "__main__":
    main() 
