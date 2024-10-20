# Sample Hardhat Project

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a Hardhat Ignition module that deploys that contract.

Try running some of the following tasks:

```shell
npx hardhat help
npx hardhat test
REPORT_GAS=true npx hardhat test
npx hardhat node
npx hardhat ignition deploy ./ignition/modules/Lock.js
```


# Доделать:

Чтобы развернуть смарт-контракт на основной сети Polygon (Polygon Mainnet), вам следует выполнить несколько шагов, начиная с подготовки окружения и заканчивая развертыванием контракта. Вот подробное руководство.

### Шаг 1: Установите необходимые инструменты

1. Node.js: Убедитесь, что у вас установлен Node.js. Он нужен для работы с Hardhat и другими инструментами разработки.

2. Hardhat: Если вы еще не установили Hardhat, создайте новый проект и установите его:

   mkdir MyPolygonProject
   cd MyPolygonProject
   npm init -y
   npm install --save-dev hardhat

   Запустите команду для инициализации Hardhat:

   npx hardhat

### Шаг 2: Установите необходимые зависимости

Установите библиотеки OpenZeppelin (если вы используете их для разработке):

npm install @openzeppelin/contracts

Также установите зависимости для взаимодействия с сетью и верификации контрактов:

npm install @nomiclabs/hardhat-ethers ethers dotenv

### Шаг 3: Настройте файл hardhat.config.js

Добавьте настройки для основной сети Polygon в файл hardhat.config.js. Вам нужно указать URL RPC-сервера Polygon и свой приватный ключ для доступа к кошельку.

Пример файла hardhat.config.js:

require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-etherscan");
require("dotenv").config();

module.exports = {
  solidity: "0.8.0",
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

### Шаг 4: Создайте файл .env

Создайте файл .env в корне вашего проекта для хранения конфиденциальных данных:

PRIVATE_KEY=ваш_приватный_ключ_кошелька
POLYGONSCAN_API_KEY=ваш_api_ключ_для_verification

Важно: Никогда не делитесь своим приватным ключом и не загружайте его в публичные репозитории.

### Шаг 5: Напишите скрипт для развертывания

Создайте файл scripts/deploy.js и добавьте в него следующий код, чтобы развернуть ваш контракт:

async function main() {
  const Itkomi = await ethers.getContractFactory("Itkomi");
  const itkomi = await Itkomi.deploy(); // Добавьте параметры конструктора, если они есть

  await itkomi.deployed();
  console.log("Contract deployed to:", itkomi.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

### Шаг 6: Развернуть контракт

Теперь, когда все готово, вы можете развернуть контракт на Polygon Mainnet, выполнив следующую команду:

npx hardhat run scripts/deploy.js --network polygon

### Шаг 7: Верификация контракта на Polygonscan

После успешного развертывания вы можете верифицировать контракт на Polygonscan, чтобы подтвердить, что код контракта совпадает с развернутым. Используйте следующую команду:

npx hardhat verify --network polygon <адрес_вашего_контракта> "constructor_parameter_1" "constructor_parameter_2"

Замените <адрес_вашего_контракта> на реальный адрес, полученный после развертывания контракта.
