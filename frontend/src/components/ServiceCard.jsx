import { Link } from 'react-router-dom'
export default function ServiceCard({service, favorites, toggle}) {
  return <article className="card"><h3><Link to={'/services/' + service.id}>{service.name}</Link></h3>
    <p>{service.category_name}</p><p>{service.price} ₽ · {service.duration_minutes} мин.</p>
    <p>{service.is_available ? 'Доступна' : 'Недоступна'}</p>
    <button type="button" onClick={() => toggle(service.id)}>{favorites.includes(service.id) ? 'Убрать из избранного' : 'В избранное'}</button>
  </article>
}
