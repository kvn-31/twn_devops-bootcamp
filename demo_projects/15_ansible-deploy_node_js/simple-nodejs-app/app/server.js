var express = require('express');
const pino = require('pino');

var app = express();

const logger = pino({ level: 'info' });

logger.info('hello world');
logger.info('This is a nodejs app for testing');

app.listen(3000, function () {
    logger.info("app listening on port 3000!");
});
