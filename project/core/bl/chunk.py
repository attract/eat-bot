import gc
from django.core.exceptions import ObjectDoesNotExist


def queryset_iterator(queryset, chunk_size=1000, return_chunk_rows=False):
    """
    Iterate over a Django Queryset ordered by the primary key
    This method loads a maximum of chunk_size (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    Note that the implementation of the iterator does not support ordered query sets.
    """
    try:
        last_pk = queryset.order_by('-pk')[:1].get().pk
    except ObjectDoesNotExist:
        return

    pk = 0
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        chunk_rows = queryset.filter(pk__gt=pk)[:chunk_size]
        for row in chunk_rows:
            pk = row.pk
            if not return_chunk_rows:
                yield row
        if return_chunk_rows:
            yield chunk_rows
        gc.collect()
