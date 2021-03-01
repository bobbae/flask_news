var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
	console.log('serving route /users');
	res.json(['A', 'B', 'C', 'D', 'E']);
});

module.exports = router;
