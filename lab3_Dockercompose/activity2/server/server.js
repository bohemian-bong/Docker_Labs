const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const app = express();
const PORT = process.env.PORT || 3000;
const cors = require('cors');

// Middleware
app.use(bodyParser.json());
app.use(cors());
// Routes
const todoRoutes = require('./routes/todoRoutes');
app.use('/api/todos', todoRoutes);

// Database Connection
const mongoHost = process.env.MONGODB_CONTAINER_HOST; // Use 'localhost' as fallback
const mongoURI = `mongodb://${mongoHost}/todolist`;
mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('MongoDB Connected');
}).catch(err => {
  console.log(mongoURI)
  console.log('MongoDB Connection Error:', err);
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
