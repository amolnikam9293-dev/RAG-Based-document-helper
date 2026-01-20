[Skip to content](https://developers.llamaindex.ai/python/examples/vector_stores/awsdocdbdemo/#_top)
# Test delete 
if ref_doc_id: store.delete(ref_doc_id) print(store._collection.count_documents({}))
