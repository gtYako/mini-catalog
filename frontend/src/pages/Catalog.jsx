import { useEffect, useState } from 'react'
import { api } from '../api/client'
import useDebounce from '../hooks/useDebounce'
import Loading from '../components/Loading'
import Filters from '../components/Filters'
import ServiceCard from '../components/ServiceCard'
const initial = {search:'', category:'', is_available:'', min_price:'', max_price:'', ordering:'', page:1}
export default function Catalog({favorites, toggle}) {
  const [filters, setFilters] = useState(initial), [categories, setCategories] = useState([])
  const [result, setResult] = useState(null), [error, setError] = useState(''), [loading, setLoading] = useState(true), [retry, setRetry] = useState(0)
  const search = useDebounce(filters.search)
  useEffect(() => { api('/categories/').then(r => setCategories(r.results)).catch(() => setError('Не удалось загрузить категории.')) }, [retry])
  useEffect(() => {
    let active = true; setLoading(true); setError('')
    const params = new URLSearchParams()
    Object.entries({...filters, search}).forEach(([key, value]) => { if (value !== '') params.set(key, value) })
    api('/services/?' + params).then(data => { if (active) setResult(data) }).catch(e => { if (active) setError(e.message) }).finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [filters.category, filters.is_available, filters.min_price, filters.max_price, filters.ordering, filters.page, search, retry])
  return <><h1>Каталог услуг</h1><Filters values={filters} setValues={setFilters} categories={categories}/>
    <p>Посетителям показываются только доступные услуги.</p>
    {loading ? <Loading/> : error ? <div role="alert">{error} <button onClick={() => setRetry(retry + 1)}>Повторить</button></div> : <>
      {!result?.results.length ? <p>Услуги не найдены.</p> : <div className="cards">{result.results.map(s => <ServiceCard key={s.id} service={s} favorites={favorites} toggle={toggle}/>)}</div>}
      <div className="pagination"><button disabled={!result?.previous} onClick={() => setFilters({...filters,page:filters.page-1})}>Назад</button><span>Страница {filters.page} · найдено {result?.count}</span><button disabled={!result?.next} onClick={() => setFilters({...filters,page:filters.page+1})}>Далее</button></div>
    </>}
  </>
}
