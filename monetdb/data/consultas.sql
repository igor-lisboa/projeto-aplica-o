-- Cada execução tem um id em dataflow e seu timestamp em dataflow_execution: consulta de tempos de execução para cada execução realizada.
-- todas as execucoes foram executadas em pipeline ou houve paralelismo na execucao ?
select
	t.id,
	t.next_execution_datetime,
	t.execution_datetime,
	COALESCE(t.next_execution_datetime,t.execution_datetime) - t.execution_datetime as execution_time
from
	(
	select
		d.id,
		LEAD( sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') ) over (
	order by
		de.execution_datetime,
		d.id) as next_execution_datetime,
		sys.str_to_timestamp(de.execution_datetime, '%Y-%m-%d %H:%M:%S') as execution_datetime
	from
		dataflow d
	left join dataflow_execution de on
		(d.id = de.df_id)
	order by
		de.execution_datetime,
		d.id) t
order by
	execution_time,t.id;
