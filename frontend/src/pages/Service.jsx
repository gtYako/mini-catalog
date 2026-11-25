import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api/client'
import Loading from '../components/Loading'
export default function Service() {
  const {id} = useParams(), [service, setService] = useState(null), [error, setError] = useState(''), [loading, setLoading] = useState(true), [retry, setRetry] = useState(0)
  useEffect(() => { setLoading(true); setError(''); api('/services/' + id + '/').then(setService).catch(e => setError(e.message)).finally(() => setLoading(false)) }, [id, retry])
  if (loading) return <Loading/>
  if (error) return <div role="alert">{error} <button onClick={() => setRetry(retry+1)}>Повторить</button></div>
  return <><Link to="/">← Каталог</Link><h1>{service.name}</h1><p>{service.description}</p><p>Категория: {service.category_name}</p><p>Цена: {service.price} ₽</p><p>Длительность: {service.duration_minutes} минут</p><p>{service.is_available ? 'Доступна' : 'Недоступна'}</p>{service.is_available && <Link className="button" to={'/request?service=' + service.id}>Оставить заявку</Link>}</>
}
