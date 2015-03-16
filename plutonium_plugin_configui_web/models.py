
import sys
from sqlchemyforms.validators.is_in_db import IsInDBValidator
from sqlchemyforms.validators.is_in_set import IsInSetValidator
from sqlchemyforms.field import Field
from sqlchemyforms.table.column import Column
from plutonium.modules.tools import Storage

Feed = getattr(sys.modules['plutonium.models.feed'], 'Feed')
Output = getattr(sys.modules['plutonium.models.output'], 'Output')
Filter = getattr(sys.modules['plutonium.models.filter'], 'Filter')

Feed.form_field_definitions = [
    Field(Feed.id),
    Field(Feed.url),
    Field(Feed.name),
    Field(Feed.enabled),
    Field(Feed.output, [IsInDBValidator(Output.id, [Output.type])]),
    Field(Feed.update_interval),
    Field(Feed.target_path_pattern),
    Field(Feed.filters, [IsInDBValidator(Filter.id, [Filter.name], multiple = True)]),
]

Feed.table_definitions = Storage(
    columns = [
        Column(Feed.id),
        Column(Feed.enabled),
        Column(Feed.name),
        Column(Feed.url),
        Column(Feed.update_interval),
        Column(Feed.target_path_pattern),
        Column(Feed.last_update),
        Column(Feed.output, fetcher = lambda v: v.name),
        Column(Feed.filters, fetcher = lambda v: len(v))
    ],
    sorting_defaults = Storage(
        key = Feed.id,
        dir = 'asc'
    ),
    row_per_page = 20
)

Output.form_field_definitions = [
    Field(Output.id),
    Field(Output.name),
    Field(Output.type, [IsInSetValidator(lambda : {val: {'name': val} for val in Output.output_plugins.keys()})]),
    Field(Output.params),
]

Filter.form_field_definitions = [
    Field(Filter.id),
    Field(Filter.name),
    Field(Filter.pattern),
    Field(Filter.source_node),
    Field(Filter.type),
]

