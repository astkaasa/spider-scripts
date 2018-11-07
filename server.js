const http = require('http');

const hostname = '127.0.0.1';
const port = 8080;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`Route requested: ${req.url}`);
  ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
  console.log(`Receive ${req.method} method requesting ${req.url} from ${req}`);
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
