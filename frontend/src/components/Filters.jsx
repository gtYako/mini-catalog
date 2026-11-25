export default function Filters({values, setValues, categories}) {
  const change = e => setValues({...values, [e.target.name]: e.target.value, page: 1})
  return <div className="filters">
    <label>Поиск<input name="search" value={values.search} onChange={change} placeholder="Название или описание" /></label>
    <label>Категория<select name="category" value={values.category} onChange={change}><option value="">Все категории</option>{categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label>
    <label>Доступность<select name="is_available" value={values.is_available} onChange={change}><option value="">Все доступные</option><option value="true">Доступные</option><option value="false">Недоступные</option></select></label>
    <label>Цена от<input type="number" min="0" name="min_price" value={values.min_price} onChange={change}/></label>
    <label>Цена до<input type="number" min="0" name="max_price" value={values.max_price} onChange={change}/></label>
    <label>Сортировка<select name="ordering" value={values.ordering} onChange={change}><option value="">По умолчанию</option><option value="price">Сначала дешевле</option><option value="-price">Сначала дороже</option></select></label>
  </div>
}
