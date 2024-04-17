# Chainlit-Coze Integration

This repository contains an integration between Chainlit and Coze, allowing you to create a chatbot application that leverages the Coze API for generating responses.

## Overview

The chatbot application is built using Chainlit, a framework for creating interactive AI applications. It integrates with the Coze API to generate responses based on the user's input and the chat history.

## Features

- Seamless integration between Chainlit and Coze API
- Streaming responses for a more interactive user experience
- Handling of token quota errors from the Coze API
- Storing and updating chat history for context-aware conversations

## Prerequisites

Before running the application, make sure you have the following:

- Python 3.x installed
- Chainlit package installed (`pip install chainlit`)
- Coze API key and bot ID

## Setup

1. Clone the repository:

```
git clone https://github.com/lukeslp/chainlit-coze.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Coze API key and bot ID:

```
COZE_API_KEY=your_api_key
COZE_BOT_ID=your_bot_id
```

4. Run the application:

```
chainlit run app.py
```

## Deployment

The application can be deployed using Fly.io. The `fly.toml` file contains the necessary configuration for deploying the application.

To deploy the application:

1. Install the Fly CLI (https://fly.io/docs/getting-started/installing-flyctl/)

2. Log in to your Fly account:

```
fly auth login
```

3. Create a new app:

```
fly apps create chainlit-coze
```

4. Deploy the application:

```
fly deploy
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Chainlit](https://chainlit.io/) for providing the framework for building interactive AI applications
- [Coze](https://coze.com/) for providing the API for generating chatbot responses

## Contact

For any questions or inquiries, please contact [Lucas "Luke" Steuber](https://github.com/lukeslp).