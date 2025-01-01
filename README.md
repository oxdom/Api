# OX.FUN API

Welcome to the OX.FUN API documentation. This API provides a set of endpoints to interact with the OX.FUN platform, allowing developers to integrate and extend its functionalities.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The OX.FUN API is designed to provide developers with access to the core features of the OX.FUN platform. It is a RESTful API that supports JSON format for requests and responses.

## Getting Started

To start using the OX.FUN API, you will need to obtain an API key. Please refer to the [API documentation](https://oxoxox.gitbook.io/ox-docs/api/restapi) for detailed instructions on how to acquire an API key and authenticate your requests.

## API Endpoints

Below is a list of available API endpoints. For detailed information on each endpoint, please refer to the [API documentation](https://oxoxox.gitbook.io/ox-docs).

- `GET /api/v1/resource` - Description of the endpoint.
- `POST /api/v1/resource` - Description of the endpoint.
- `PUT /api/v1/resource/:id` - Description of the endpoint.
- `DELETE /api/v1/resource/:id` - Description of the endpoint.

## Contributing

We welcome contributions from the community. If you would like to contribute, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or support, please contact us on [support.ox.fun](https://support.ox.fun).

<details>
  <summary>REST API v3 Format</summary>

  For detailed information on the REST API v3 format, please refer to the [OX Docs](https://oxoxox.gitbook.io/ox-docs/api/restapi).

  ### Example Endpoints

  - **Market Depth**
    - `GET /v3/depth?marketCode={marketCode}`
      - JavaScript Example: `fetchMarketDepth('BTC-USD-SWAP-LIN', 10)`
        - Code reference: `market-data-public/depth/depth.js`
      - Python Example: `fetch_market_depth('BTC-USD-SWAP-LIN', 10)`
        - Code reference: `market-data-public/depth/depth.py`
        

  - **Candle Data**
    - `GET /v3/candles?marketCode={marketCode}&timeframe={timeframe}&limit={limit}&startTime={startTime}&endTime={endTime}`
      - JavaScript Example: `fetchCandleData('BTC-USD-SWAP-LIN', '3600s', 100)`
        - Code reference: `market-data-public/candles/candles.js`
          - startLine: 3
          - endLine: 28
      - Python Example: `fetch_candle_data('BTC-USD-SWAP-LIN', '3600s', 100)`
        - Code reference: `market-data-public/candles/candles.py`
          - startLine: 4
          - endLine: 27

</details>
