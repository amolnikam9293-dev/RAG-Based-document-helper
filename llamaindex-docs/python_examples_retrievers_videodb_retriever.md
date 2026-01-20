[Skip to content](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#_top)
# connect to VideoDB 
conn = connect() coll = conn.create_collection( name=“VideoDB Retrievers”, description=“VideoDB Retrievers” )
# upload videos to default collection in VideoDB
[Section titled “upload videos to default collection in VideoDB”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#upload-videos-to-default-collection-in-videodb)
print(“Uploading Video”) video = coll.upload(url=“<https://www.youtube.com/watch?v=aRgP3n0XiMc>”) print(f”Video uploaded with ID: {video.id}“)
# video = coll.get_video(“m-b6230808-307d-468a-af84-863b2c321f05”)
[Section titled “video = coll.get_video(“m-b6230808-307d-468a-af84-863b2c321f05”)”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#video--collget_videom-b6230808-307d-468a-af84-863b2c321f05)
```


Uploading Video




Video uploaded with ID: m-a758f9bb-f769-484a-9d54-02417ccfe7e6





> * `coll = conn.get_collection()` : Returns default collection object.


> * `coll.get_videos()` : Returns list of all the videos in a collections.


> * `coll.get_video(video_id)`: Returns Video object from given`video_id`.



### 🗣️ Step 2: Indexing & Search from Spoken Content



Video can be viewed as data with different modalities. First, we will work with the `spoken content`.



#### 🗣️ Indexing Spoken Content




```python


print("Indexing spoken content in Video...")


video.index_spoken_words()

```

```

Indexing spoken content in Video...




100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:48<00:00,  2.08it/s]

```

#### 🗣️ Retrieving Relevant Nodes from Spoken Index
[Section titled “🗣️ Retrieving Relevant Nodes from Spoken Index”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-retrieving-relevant-nodes-from-spoken-index)
We will use the `VideoDBRetriever` to retrieve relevant nodes from our indexed content. The video ID should be passed as a parameter, and the `index_type` should be set to `IndexType.spoken_word`.
You can configure the `score_threshold` and `result_threshold` after experimentation.
```


from llama_index.retrievers.videodb import VideoDBRetriever




from videodb import SearchType, IndexType





spoken_retriever =VideoDBRetriever(




collection=coll.id,




video=video.id,




search_type=SearchType.semantic,




index_type=IndexType.spoken_word,




score_threshold=0.1,






spoken_query ="Nationwide exams"




nodes_spoken_index = spoken_retriever.retrieve(spoken_query)


```

#### 🗣️️️ Viewing the result : 💬 Text
[Section titled “🗣️️️ Viewing the result : 💬 Text”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F%EF%B8%8F%EF%B8%8F-viewing-the-result---text)
We will use the relevant nodes and synthesize the response using llamaindex
```


from llama_index.core import get_response_synthesizer





response_synthesizer =get_response_synthesizer()





response = response_synthesizer.synthesize(




spoken_query,nodes=nodes_spoken_index





print(response)


```

```

The results of the nationwide exams were eagerly awaited all day.

```

#### 🗣️ Viewing the result : 🎥 Video Clip
[Section titled “🗣️ Viewing the result : 🎥 Video Clip”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-viewing-the-result---video-clip)
For each retrieved node that is relevant to the query, the `start` and `end` fields in the metadata represent the time interval covered by the node.
We will use VideoDB’s Programmable Stream to generate a stream of relevant video clips based on the timestamps of these nodes.
```


from videodb import play_stream





results =[




(node.metadata["start"], node.metadata["end"])




for node in nodes_spoken_index






stream_link = video.generate_stream(results)




play_stream(stream_link)


```

```

'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/3c108acd-e459-494a-bc17-b4768c78e5df.m3u8'

```

### 📸️ Step3 : Index & Search from Visual Content
[Section titled “📸️ Step3 : Index & Search from Visual Content”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-step3--index--search-from-visual-content)
#### 📸 Indexing Visual Content
[Section titled “📸 Indexing Visual Content”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-indexing-visual-content)
To learn more about Scene Index, explore the following guides:
  * [Quickstart Guide](https://github.com/video-db/videodb-cookbook/blob/main/quickstart/Scene%20Index%20QuickStart.ipynb) guide provides a step-by-step introduction to Scene Index. It’s ideal for getting started quickly and understanding the primary functions.
  * [Scene Extraction Options Guide](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/playground_scene_extraction.ipynb) delves deeper into the various options available for scene extraction within Scene Index. It covers advanced settings, customization features, and tips for optimizing scene extraction based on different needs and preferences.


```


from videodb import SceneExtractionType





print("Indexing Visual content in Video...")




# Index scene content



index_id = video.index_scenes(




extraction_type=SceneExtractionType.shot_based,




extraction_config={"frame_count": 3},




prompt="Describe the scene in detail",





video.get_scene_index(index_id)





print(f"Scene Index successful with ID: {index_id}")


```

```

Indexing Visual content in Video...


Scene Index successful with ID: 990733050d6fd4f5

```

#### 📸️ Retrieving Relevant Nodes from Scene Index
[Section titled “📸️ Retrieving Relevant Nodes from Scene Index”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-retrieving-relevant-nodes-from-scene-index)
Just like we used `VideoDBRetriever` for the spoken index, we will use it for the scene index. Here, we will need to set `index_type` to `IndexType.scene` and pass the `scene_index_id`
```


from llama_index.retrievers.videodb import VideoDBRetriever




from videodb import SearchType, IndexType






scene_retriever =VideoDBRetriever(




collection=coll.id,




video=video.id,




search_type=SearchType.semantic,




index_type=IndexType.scene,




scene_index_id=index_id,




score_threshold=0.1,






scene_query ="accident scenes"




nodes_scene_index = scene_retriever.retrieve(scene_query)


```

#### 📸️️️ Viewing the result : 💬 Text
[Section titled “📸️️️ Viewing the result : 💬 Text”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F%EF%B8%8F%EF%B8%8F-viewing-the-result---text-1)
```


from llama_index.core import get_response_synthesizer





response_synthesizer =get_response_synthesizer()





response = response_synthesizer.synthesize(




scene_query,nodes=nodes_scene_index





print(response)


```

```

The scenes described do not depict accidents but rather dynamic and intense scenarios involving motion, urgency, and tension in urban settings at night.

```

#### 📸 ️ Viewing the result : 🎥 Video Clip
[Section titled “📸 ️ Viewing the result : 🎥 Video Clip”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-%EF%B8%8F-viewing-the-result---video-clip)
```


from videodb import play_stream





results =[




(node.metadata["start"], node.metadata["end"])




for node in nodes_scene_index






stream_link = video.generate_stream(results)




play_stream(stream_link)


```

```

'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/ae74e9da-13bf-4056-8cfa-0267087b74d7.m3u8'

```

### 🛠️ Step4: Simple Multimodal RAG - Combining Results of Both modalities
[Section titled “🛠️ Step4: Simple Multimodal RAG - Combining Results of Both modalities”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-step4-simple-multimodal-rag---combining-results-of-both-modalities)
We want to unlock in multimodal queries in our video library like this:
> 📸🗣️ “ _Show me 1.Accident Scene 2.Discussion about nationwide exams_ ”
There are lots of way to do create a multimodal RAG, for the sake of simplicity we are choosing a simple approach:
  1. 🧩 **Query Transformation** : Divide query into two parts that can be used with respective scene and spoken indexes.
  2. 🔎 **Finding Relevant nodes for each modality** : Using `VideoDBRetriever` find relevant nodes from Spoken Index and Scene Index
  3. ✏️ **Viewing the result : Text** : Use Relevant Nodes to sythesize a text reponse Integrating the results from both indexes for precise video segment identification.
  4. 🎥 **Viewing the result : Video Clip** : Integrating the results from both indexes for precise video segment identification.


> To checkout more advanced multimodal techniques, checkout out [advnaced multimodal guides](https://docs.videodb.io/multimodal-guide-90)
#### 🧩 Query Transformation
[Section titled “🧩 Query Transformation”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-query-transformation)
```


from llama_index.llms.openai import OpenAI






defsplit_spoken_visual_query(query):




transformation_prompt ="""




Divide the following query into two distinct parts: one for spoken content and one for visual content. The spoken content should refer to any narration, dialogue, or verbal explanations and The visual content should refer to any images, videos, or graphical representations. Format the response strictly as:\nSpoken: <spoken_query>\nVisual: <visual_query>\n\nQuery: {query}





prompt = transformation_prompt.format(query=query)




response =OpenAI(model="gpt-4").complete(prompt)




divided_query = response.text.strip().split("\n")




spoken_query = divided_query[0].replace("Spoken:","").strip()




scene_query = divided_query[1].replace("Visual:","").strip()




return spoken_query, scene_query






query ="Show me 1.Accident Scene 2.Discussion about nationwide exams "




spoken_query, scene_query =split_spoken_visual_query(query)




print("Query for Spoken retriever : ", spoken_query)




print("Query for Scene retriever : ", scene_query)


```

```

Query for Spoken retriever :  Discussion about nationwide exams


Query for Scene retriever :  Accident Scene

```

##### 🔎 Finding Relevant nodes for each modality
[Section titled “🔎 Finding Relevant nodes for each modality”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-finding-relevant-nodes-for-each-modality)
```


from videodb import SearchType, IndexType




# Retriever for Spoken Index



spoken_retriever =VideoDBRetriever(




collection=coll.id,




video=video.id,




search_type=SearchType.semantic,




index_type=IndexType.spoken_word,




score_threshold=0.1,





# Retriever for Scene Index



scene_retriever =VideoDBRetriever(




collection=coll.id,




video=video.id,




search_type=SearchType.semantic,




index_type=IndexType.scene,




scene_index_id=index_id,




score_threshold=0.1,





# Fetch relevant nodes for Spoken index



nodes_spoken_index = spoken_retriever.retrieve(spoken_query)




# Fetch relevant nodes for Scene index



nodes_scene_index = scene_retriever.retrieve(scene_query)


```

#### ️💬️ Viewing the result : Text
[Section titled “️💬️ Viewing the result : Text”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F%EF%B8%8F-viewing-the-result--text)
```


response_synthesizer =get_response_synthesizer()





response = response_synthesizer.synthesize(




query,nodes=nodes_scene_index + nodes_spoken_index





print(response)


```

```

The first scene depicts a dynamic and intense scenario in an urban setting at night, involving a motorcycle chase with a figure possibly dodging away. The second scene portrays a dramatic escape or rescue situation with characters in motion alongside a large truck. The discussion about nationwide exams involves a conversation between a character and their mother about exam results and studying.

```

#### 🎥 Viewing the result : Video Clip
[Section titled “🎥 Viewing the result : Video Clip”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-viewing-the-result--video-clip)
From each modality, we have retrieved results that are relevant to the query within that specific modality (semantic and scene/visual, in this case).
Each node has start and end fields in the metadata, which represent the time interval the node covers.
There are lots of way to sythesize there results, For now we will use a simple method :
  * `Union`: This method takes all the timestamps from every node, creating a comprehensive list that includes every relevant time, even if some timestamps appear in only one modality.


One of the other ways can be `Intersection`:
  * `Intersection`: This method only includes timestamps that are present in every node, resulting in a smaller list with times that are universally relevant across all modalities.


```


from videodb import play_stream






defmerge_intervals(intervals):




ifnot intervals:




return[]




intervals.sort=lambdax: x[0])




merged =[intervals[0]]




for interval in intervals[1:]:




if interval[0] <= merged[-1][1]:




merged[-1][1]=max(merged[-1][1], interval[1])




else:




merged.append(interval)




return merged





# Extract timestamps from both relevant nodes



results =[




[node.metadata["start"], node.metadata["end"]]




for node in nodes_spoken_index + nodes_scene_index





merged_results =merge_intervals(results)




# Use Videodb to create a stream of relevant clips



stream_link = video.generate_stream(merged_results)




play_stream(stream_link)


```

```

'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/91b08b39-c72f-4e33-ad1c-47a2ea11ac17.m3u8'

```

## 🛠 Using VideoDBRetriever to Build RAG for Collection of Videos
[Section titled “🛠 Using VideoDBRetriever to Build RAG for Collection of Videos”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-using-videodbretriever-to-build-rag-for-collection-of-videos)
### Adding More videos to our collection
[Section titled “Adding More videos to our collection”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#adding-more-videos-to-our-collection)
```


video_2 = coll.upload="https://www.youtube.com/watch?v=kMRX3EA68g4")


```

#### 🗣️ Indexing Spoken Content
[Section titled “🗣️ Indexing Spoken Content”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-indexing-spoken-content)
```


video_2.index_spoken_words()


```

#### 📸 Indexing Scenes
[Section titled “📸 Indexing Scenes”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-indexing-scenes)
```


from videodb import SceneExtractionType





print("Indexing Visual content in Video...")




# Index scene content



index_id = video_2.index_scenes(




extraction_type=SceneExtractionType.shot_based,




extraction_config={"frame_count": 3},




prompt="Describe the scene in detail",





video_2.get_scene_index(index_id)





print(f"Scene Index successful with ID: {index_id}")


```

```

[Video(id=m-b6230808-307d-468a-af84-863b2c321f05, collection_id=c-4882e4a8-9812-4921-80ff-b77c9c4ab4e7, stream_url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/528623c2-3a8e-4c84-8f05-4dd74f1a9977.m3u8, player_url=https://console.dev.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/528623c2-3a8e-4c84-8f05-4dd74f1a9977.m3u8, name=Death note - episode 1 (english dubbed) | HD, description=None, thumbnail_url=None, length=1366.006712),



Video(id=m-f5b86106-4c28-43f1-b753-fa9b3f839dfe, collection_id=c-4882e4a8-9812-4921-80ff-b77c9c4ab4e7, stream_url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/4273851a-46f3-4d57-bc1b-9012ce330da8.m3u8, player_url=https://console.dev.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/4273851a-46f3-4d57-bc1b-9012ce330da8.m3u8, name=Death note - episode 5 (english dubbed) | HD, description=None, thumbnail_url=None, length=1366.099592)]


```

#### 🧩 Query Transformation
[Section titled “🧩 Query Transformation”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-query-transformation-1)
```


query ="Show me 1.Accident Scene 2.Kiara is speaking "




spoken_query, scene_query =split_spoken_visual_query(query)




print("Query for Spoken retriever : ", spoken_query)




print("Query for Scene retriever : ", scene_query)


```

```

Query for Spoken retriever :  Kiara is speaking


Query for Scene retriever :  Show me Accident Scene

```

#### 🔎 Finding relevant nodes
[Section titled “🔎 Finding relevant nodes”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-finding-relevant-nodes)
```


from videodb import SearchType, IndexType




# Retriever for Spoken Index



spoken_retriever =VideoDBRetriever(




collection=coll.id,




search_type=SearchType.semantic,




index_type=IndexType.spoken_word,




score_threshold=0.2,





# Retriever for Scene Index



scene_retriever =VideoDBRetriever(




collection=coll.id,




search_type=SearchType.semantic,




index_type=IndexType.scene,




score_threshold=0.2,





# Fetch relevant nodes for Spoken index



nodes_spoken_index = spoken_retriever.retrieve(spoken_query)




# Fetch relevant nodes for Scene index



nodes_scene_index = scene_retriever.retrieve(scene_query)


```

#### ️💬️ Viewing the result : Text
[Section titled “️💬️ Viewing the result : Text”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F%EF%B8%8F-viewing-the-result--text-1)
```


response_synthesizer =get_response_synthesizer()





response = response_synthesizer.synthesize(




"What is kaira speaking. And tell me about accident scene",




nodes=nodes_scene_index + nodes_spoken_index,





print(response)


```

```

Kira is speaking about his plans and intentions regarding the agent from the bus. The accident scene captures a distressing moment where an individual is urgently making a phone call near a damaged car, with a victim lying motionless on the ground. The chaotic scene includes a bus in the background, emphasizing the severity of the tragic incident.

```

#### 🎥 Viewing the result : Video Clip
[Section titled “🎥 Viewing the result : Video Clip”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-viewing-the-result--video-clip-1)
When working with an editing workflow involving multiple videos, we need to create a `Timeline` of `VideoAsset` and then compile them.
```


from videodb import connect, play_stream




from videodb.timeline import Timeline




from videodb.asset import VideoAsset




# Create a new timeline Object



timeline =Timeline(conn)





for node_obj in nodes_scene_index + nodes_spoken_index:




node = node_obj.node





# Create a Video asset for each node




node_asset =VideoAsset(




asset_id=node.metadata["video_id"],




start=node.metadata["start"],




end=node.metadata["end"],






# Add the asset to timeline




timeline.add_inline(node_asset)




# Generate stream for the compiled timeline



stream_url = timeline.generate_stream()




play_stream(stream_url)


```

```

'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/2810827b-4d80-44af-a26b-ded2a7a586f6.m3u8'

```

## Configuring `VideoDBRetriever`
[Section titled “Configuring VideoDBRetriever”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#configuring-videodbretriever)
### ⚙️ Retriever for only one Video
[Section titled “⚙️ Retriever for only one Video”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-retriever-for-only-one-video)
You can pass the `id` of the video object to search in only that video.
```


VideoDBRetriever(video="my_video.id")


```

### ⚙️ Retriever for a set of Video/ Collection
[Section titled “⚙️ Retriever for a set of Video/ Collection”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-retriever-for-a-set-of-video-collection)
You can pass the `id` of the Collection to search in only that Collection.
```


VideoDBRetriever(collection="my_coll.id")


```

### ⚙️ Retriever for different type of Indexes
[Section titled “⚙️ Retriever for different type of Indexes”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-retriever-for-different-type-of-indexes)
```


from videodb import IndexType




spoken_word =VideoDBRetriever(index_type=IndexType.spoken_word)





scene_retriever =VideoDBRetriever(index_type=IndexType.scene,scene_index_id="my_index_id")


```

### ⚙️ Configuring Search Type of Retriever
[Section titled “⚙️ Configuring Search Type of Retriever”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-configuring-search-type-of-retriever)
`search_type` determines the search method used to retrieve nodes against given query
```


from videodb import SearchType, IndexType





keyword_spoken_search =VideoDBRetriever(




search_type=SearchType.keyword,




index_type=IndexType.spoken_word






semantic_scene_search =VideoDBRetriever(




search_type=SearchType.semantic,




index_type=IndexType.spoken_word



```

### ⚙️ Configure threshold parameters
[Section titled “⚙️ Configure threshold parameters”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-configure-threshold-parameters)
  * `result_threshold`: is the threshold for number of results returned by retriever; the default value is `5`
  * `score_threshold`: only nodes with score higher than `score_threshold` will be returned by retriever; the default value is `0.2`


```


custom_retriever =VideoDBRetriever(result_threshold=2,score_threshold=0.5)


```

## ✨ Configuring Indexing and Chunking
[Section titled “✨ Configuring Indexing and Chunking”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-configuring-indexing-and-chunking)
In this example, we utilize the VideoDB’s Indexing for video retrieval. However, you have the flexibility to load both Transcript and Scene Data and apply your own indexing techniques using llamaindex.
For more detailed guidance, refer to this [guide](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/multi_modal/multi_modal_videorag_videodb.ipynb).
## 🏃‍♂️ Next Steps
[Section titled “🏃‍♂️ Next Steps”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#%EF%B8%8F-next-steps)
In this guide, we built a Simple Multimodal RAG for Videos Using VideoDB, Llamaindex, and OpenAI
You can optimize the pipeline by incorporating more advanced techniques like
  * Optimize Query Transformation
  * More methods to combine retrieved nodes from different modalities
  * Experiment with Different RAG pipelines like Knowledge Graph


To learn more about Programable Stream feature that we used to create relevant clip checkout [Dynamic Video Stream Guide](https://docs.videodb.io/dynamic-video-stream-guide-44)
To learn more about Scene Index, explore the following guides:
  * [Scene Extraction Options](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/playground_scene_extraction.ipynb)
  * [Custom Annotation Pipelines](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/custom_annotations.ipynb)


## 👨‍👩‍👧‍👦 Support & Community
[Section titled “👨‍👩‍👧‍👦 Support & Community”](https://developers.llamaindex.ai/python/examples/retrievers/videodb_retriever/#-support--community)
If you have any questions or feedback. Feel free to reach out to us 🙌🏼


