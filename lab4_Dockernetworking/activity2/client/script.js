// script.js

let todos=[]

const SERVER_URL = "http://172.23.0.2:3000";
const todoList = document.getElementById('todoList');
const todoInput = document.getElementById('todoInput');

function renderTodos() {
  todoList.innerHTML = '';
  todos.forEach(todo => {
    const li = document.createElement('li');
    li.textContent = todo.text;
    if (todo.completed) {
      li.classList.add('completed');
    }
    li.addEventListener('click', () => toggleTodoComplete(todo.text));
    todoList.appendChild(li);
  });
}

async function fetchTodos() {
  const response = await fetch(`${SERVER_URL}/api/todos`);
  const todos1 = await response.json();
  todos=todos1;
  renderTodos(todos);
}

async function addTodo() {
  const text = todoInput.value;
  if (text.trim() !== '') {
    const response = await fetch(`${SERVER_URL}/api/todos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text })
    });
    const newTodo = await response.json();
    todos.push(newTodo)
    fetchTodos();
    todoInput.value = '';
  }
}

async function toggleTodoComplete(text) {
  const response = await fetch(`${SERVER_URL}/api/todos/${text}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ completed: !todos.find(todo => todo.text === text).completed })
  });
  const updatedTodo = await response.json();
  todos = todos.map(todo => (todo.text === updatedTodo.text ? updatedTodo : todo));
  renderTodos(todos);
}

fetchTodos();
