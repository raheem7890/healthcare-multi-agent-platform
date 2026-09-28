import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { deleteMemory, listMemory } from '../api/memory'

export function MemoryPage() {
  const client = useQueryClient()
  const { data = [], isLoading } = useQuery({ queryKey: ['memory'], queryFn: listMemory })
  const remove = useMutation({ mutationFn: deleteMemory, onSuccess: () => client.invalidateQueries({ queryKey: ['memory'] }) })
  return (
    <div className="page">
      <header className="page-header"><div><span className="eyebrow">Your data</span><h1>Saved memory</h1>
        <p>Review and remove consented summaries used to make future conversations more relevant.</p></div></header>
      <section className="panel">
        {isLoading ? <p>Loading…</p> : data.length === 0 ? <div className="empty-state small"><h2>No saved memories</h2><p>Nothing has been stored for long-term use.</p></div> : (
          <div className="stack">{data.map((item) => <article className="list-card" key={item.id}><div><strong>{item.memory_type.replaceAll('_', ' ')}</strong>
            <p>{item.summary_text}</p><span>{new Date(item.created_at).toLocaleDateString()}</span></div>
            <button className="text-button danger" onClick={() => window.confirm('Delete this saved memory?') && remove.mutate(item.id)}>Delete</button></article>)}</div>
        )}
      </section>
    </div>
  )
}

