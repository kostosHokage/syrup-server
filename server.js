const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;


//pm2 start server.js

app.use(express.json())

app.post('/api/save_accounts', (req, res) => {
    const { userInitial, usernames } = req.body;

    if (!userInitial || !usernames) {
        return res.status(400).send('Поля userInitial и usernames обязательны.');
    }

    const filePath = path.join('accounts.json');
    let accounts = [];

    if (fs.existsSync(filePath)) {
        accounts = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }

    accounts.push({ userInitial, usernames });

    fs.writeFileSync(filePath, JSON.stringify(accounts, null, 2));
    res.send('Аккаунты сохранены.');
});

app.get('/api/usernames', (req, res) => {
    const filePath = path.join('accounts.json');

    if (!fs.existsSync(filePath)) {
        return res.status(404).send('Файл accounts.json не найден.');
    }

    const accounts = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const usernames = accounts.flatMap(account => account.usernames);

    res.json(usernames);
});

app.get('/api/data', (req, res) => {
    const filePath = path.join('all_user_data.json');

    if (!fs.existsSync(filePath)) {
        return res.status(404).send('Файл all_user_data.json не найден.');
    }

    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    res.json(data);
});

app.get('/api/log', (req, res) => {
    const filePath = path.join('log.json');

    if (!fs.existsSync(filePath)) {
        return res.status(404).send('Файл log.json не найден.');
    }

    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    res.json(data);
});

app.delete('/api/delete_account', (req, res) => {
    const { username } = req.body;

    if (!username) {
        return res.status(400).send('Поле username обязательно.');
    }

    const filePath = path.join('accounts.json');
    let accounts = [];

    if (fs.existsSync(filePath)) {
        accounts = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }

    accounts.forEach(account => {
        account.usernames = account.usernames.filter(user => user !== username);
    });

    accounts = accounts.filter(account => account.usernames.length > 0);

    fs.writeFileSync(filePath, JSON.stringify(accounts, null, 2));
    res.send('Аккаунт удален.');
});


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
