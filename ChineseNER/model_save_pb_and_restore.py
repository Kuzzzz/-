import tensorflow as tf
import os
from tensorflow.python import pywrap_tensorflow


def model_save_pb(ckpt_path, model_meta_name, pbmodel_path, pb_model_name, model_output_nodes):
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        latest_ckpt = tf.train.latest_checkpoint(ckpt_path)

        restore_saver = tf.train.import_meta_graph(os.path.join(ckpt_path,model_meta_name))
        restore_saver.restore(sess, latest_ckpt)
        # for x in tf.global_variables():
        #     print(x)
        for node in sess.graph_def.node:
            print(node.name)
        output_graph_def = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, [model_output_nodes])
        # tf.train.write_graph(output_graph_def, pbmodel_path, pb_model_name, as_text=False)

        # another way to save graph
        with tf.gfile.GFile(os.path.join(pbmodel_path, pb_model_name), "wb") as f:
            f.write(output_graph_def.SerializeToString())


def model_pb_restore(pb_model_path):
    with tf.Session() as sess:
        with open(pb_model_path, 'rb') as graph:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(graph.read())
            output = tf.import_graph_def(graph_def, return_elements=['project/scores:0'])
            print(sess.run(output))

def model_pb(path):
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        with open(path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            print(graph_def)

if __name__ == "__main__":
    ckpt_path = "./ckpt6"
    model_meta_name = "ner1.ckpt.meta"
    pb_to_path = "./pbmodels"
    model_save_pb(ckpt_path, model_meta_name, pb_to_path, "ner_model6.pb", "project/scores")
    # model_pb_restore(os.path.join(pb_to_path, "ner_model.pb"))
    # model_pb('./pbmodels/ner_model6.pb')
