const express = require('express');
const app = express();
app.use(express.json());

app.get('/api/mensagem', (req, res) => {
  res.json({ mensagem: 'Olá, esta é sua API!' });
});

app.listen(3000, () => console.log('Servidor rodando na porta 3000'));
