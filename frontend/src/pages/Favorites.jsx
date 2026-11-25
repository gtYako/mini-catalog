import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import Loading from '../components/Loading'
import ServiceCard from '../components/ServiceCard'

export default function Favorites({ favorites, toggle }) {
  const [items, setItems] = useState([])
  const [missing, setMissing] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [retry, setRetry] = useState(0)

  useEffect(() => {
    if (!favorites.length) { setItems([]); setMissing([]); setError(''); setLoading(false); return }
    let active = true
    setLoading(true)
    setError('')
    Promise.allSettled(favorites.map(id => api('/services/' + id + '/'))).then(results => {
      if (!active) return
      const failed = results.find(result => result.status === 'rejected' && result.reason.status !== 404)
      if (failed) { setError(failed.reason.message); return }
      setItems(results.filter(result => result.status === 'fulfilled').map(result => result.value))
      setMissing(favorites.filter((id, index) => results[index].status === 'rejected'))
    }).finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [favorites, retry])

  return <><h1>Избранное</h1>
    <p>Избранное хранится только в этом браузере.</p>
    {!favorites.length ? <p>Пока ничего нет. <Link to="/">Перейти в каталог</Link></p> :
      loading ? <Loading/> : error ? <div role="alert">{error} <button onClick={() => setRetry(retry + 1)}>Повторить</button></div> : <>
        <div className="cards">{items.map(service => <ServiceCard key={service.id} service={service} favorites={favorites} toggle={toggle}/>)}</div>
        {missing.map(id => <p key={id}>Услуга №{id} удалена или недоступна. <button onClick={() => toggle(id)}>Убрать из избранного</button></p>)}
      </>}
  </>
}
