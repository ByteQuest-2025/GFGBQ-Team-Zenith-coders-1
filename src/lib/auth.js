export const saveUser = (user) => {
  localStorage.setItem('user', JSON.stringify(user));
  localStorage.setItem('auth_token', user.token);
};

export const getUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

export const removeUser = () => {
  localStorage.removeItem('user');
  localStorage.removeItem('auth_token');
};

export const getToken = () => {
  return localStorage.getItem('auth_token');
};

export const isAuthenticated = () => {
  return !!getToken();
};