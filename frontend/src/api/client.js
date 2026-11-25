const base = import.meta.env.VITE_API_URL || '/api'
function cookie(name) {
  const part = document.cookie.split('; ').find(item => item.startsWith(name + '='))
  return part ? decodeURIComponent(part.split('=').slice(1).join('=')) : ''
}
export async function api(path, options = {}) {
  const method = options.method || 'GET'
  const headers = { ...options.headers }
  if (options.body) headers['Content-Type'] = 'application/json'
  if (!['GET', 'HEAD'].includes(method)) headers['X-CSRFToken'] = cookie('csrftoken')
  let response
  try { response = await fetch(base + path, { ...options, method, headers, credentials: 'same-origin' }) }
  catch { throw { message: 'Не удалось подключиться к серверу. Проверьте, запущен ли Django.' } }
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const messages = {400: 'Проверьте введённые данные.', 403: 'Нет доступа. Войдите как администратор.', 404: 'Запись не найдена.', 500: 'Ошибка сервера. Попробуйте позже.'}
    throw { status: response.status, data, message: data.detail || messages[response.status] || 'Ошибка запроса.' }
  }
  return data
}
export function fieldError(errors, field) {
  const value = errors?.[field]
  return Array.isArray(value) ? value.join(' ') : value || ''
}
