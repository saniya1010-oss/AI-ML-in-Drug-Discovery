# Drug repurposing or Reposioning 

Drug repurpoing means finding new therapeutic uses for existing drugs,
instead of discovering new compounds which can take years and is cost ineffective.
The process typically involves:
- Taking drugs that are already approved
- Find if these drugs can work for something else

# Common AI/ML approaches to Drug Repurposing

  | Approach                                   | What It Does                                                                                                                  | Example ML/AI Tools                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **1. Similarity-based models**             | Find drugs that have similar molecular structure, gene expression, or side-effect profiles to drugs known to treat a disease. | Cosine similarity, KNN, clustering |
| **2. Network-based models**                | Build graphs linking drugs–targets–diseases and find new connections.                                                         | Graph Neural Networks (GNNs), Network propagation        |
| **3. Transcriptomic signature matching**   | Compare how drugs and diseases affect gene expression.                                                                        | Deep learning on omics data                              |
| **4. Knowledge graph / embedding methods** | Use graph embeddings from biomedical literature or databases (DrugBank, PubChem, etc.) to predict new links.                  | Node2Vec, DeepWalk, Transformers                         |
| **5. Multi-modal deep learning**           | Combine chemical structure + biological + clinical data.                                                                      | Deep learning, Autoencoders                              |
