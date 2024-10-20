require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-etherscan");
require("dotenv").config();

module.exports = {
  solidity: "0.8.26",
  networks: {
    polygon: {
      url: "https://rpc-mainnet.matic.network", // RPC URL для ведущей сети Polygon
      accounts: [process.env.PRIVATE_KEY], // Массив с приватным ключом вашего кошелька
    },
  },
  etherscan: {
    apiKey: process.env.POLYGONSCAN_API_KEY, // API ключ для верификации на Polygonscan
  },
};
