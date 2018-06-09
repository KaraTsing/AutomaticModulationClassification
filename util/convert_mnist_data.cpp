// This script converts the MNIST dataset to a lmdb (default) or
// leveldb (--backend=leveldb) format used by caffe to load data.
// Usage:
//    convert_mnist_data [FLAGS] input_image_file input_label_file
//                        output_db_file
// The MNIST dataset could be downloaded at
//    http://yann.lecun.com/exdb/mnist/

#include <gflags/gflags.h>
#include <glog/logging.h>
#include <google/protobuf/text_format.h>

#if defined(USE_LEVELDB) && defined(USE_LMDB)
#include <leveldb/db.h>
#include <leveldb/write_batch.h>
#include <lmdb.h>
#endif

#include <stdint.h>
#include <sys/stat.h>

#include <fstream>  // NOLINT(readability/streams)
#include <string>

#include "boost/scoped_ptr.hpp"
#include "caffe/proto/caffe.pb.h"
#include "caffe/util/db.hpp"
#include "caffe/util/format.hpp"

#if defined(USE_LEVELDB) && defined(USE_LMDB)

using namespace caffe;  // NOLINT(build/namespaces)
using boost::scoped_ptr;
using std::string;

DEFINE_string(backend, "lmdb", "The backend for storing the result");

// mine was written in little-endian where mnist was big. Don't use-->
uint32_t swap_endian(uint32_t val) {
    val = ((val << 8) & 0xFF00FF00) | ((val >> 8) & 0xFF00FF);
    return (val << 16) | (val >> 16);
}

union char2float
{
  float f;
  unsigned char c[4];
};

// assumes char_arr is length 4, make sure matches little endian
float char_arr_2_float(char char_arr[])
{
  char2float cf;
  cf.c[0] = char_arr[0];
  cf.c[1] = char_arr[1];
  cf.c[2] = char_arr[2];
  cf.c[3] = char_arr[3];
 
  return cf.f;
}

void convert_dataset(const char* image_filename, const char* label_filename,
        const char* db_path, const string& db_backend) {
  // Open files
  std::ifstream image_file(image_filename, std::ios::in | std::ios::binary);
  std::ifstream label_file(label_filename, std::ios::in | std::ios::binary);
  CHECK(image_file) << "Unable to open file " << image_filename;
  CHECK(label_file) << "Unable to open file " << label_filename;
  // Read the magic and the meta data
  uint32_t magic;
  uint32_t num_items;
  uint32_t num_labels;
  uint32_t rows;
  uint32_t cols;

  // check the magic value of the image file
  image_file.read(reinterpret_cast<char*>(&magic), 4);
  //magic = swap_endian(magic);
  CHECK_EQ(magic, 2051) << "Incorrect image file magic.";

  // check the magic value of the label file
  label_file.read(reinterpret_cast<char*>(&magic), 4);
  //magic = swap_endian(magic);
  CHECK_EQ(magic, 2051) << "Incorrect label file magic.";

  // check num items of the image file
  image_file.read(reinterpret_cast<char*>(&num_items), 4);
  //num_items = swap_endian(num_items);

  // check num labels from the label file
  label_file.read(reinterpret_cast<char*>(&num_labels), 4);
  //num_labels = swap_endian(num_labels);
  CHECK_EQ(num_items, num_labels);

  // check num rows in an image
  image_file.read(reinterpret_cast<char*>(&rows), 4);
  //rows = swap_endian(rows);

  // check num columns in an image
  image_file.read(reinterpret_cast<char*>(&cols), 4);
  //cols = swap_endian(cols);

  // setup references to the database
  scoped_ptr<db::DB> db(db::GetDB(db_backend));
  db->Open(db_path, db::NEW);
  scoped_ptr<db::Transaction> txn(db->NewTransaction());

  // Storing to db
  char label;
  char* pixels = new char[rows * cols * 4]; // can i just make this float?
  LOG(INFO) << "num pixels: " << rows*cols*4;
  int count = 0;
  string value;
  //float fbuff[rows*cols];

  // one image is considered a datum, num_items for me should be 110k
  Datum datum;
  //datum.set_channels(1);
  //datum.set_height(rows);
  //datum.set_width(cols);
  LOG(INFO) << "A total of " << num_items << " items.";
  LOG(INFO) << "Rows: " << rows << " Cols: " << cols;
    
  for (int item_id = 0; item_id < num_items; ++item_id) {
      datum.set_channels(1);
      datum.set_height(rows);
      datum.set_width(cols);
    
    google::protobuf::RepeatedField<float>* datumFloatData = datum.mutable_float_data();
    
    image_file.read(pixels, rows * cols* 4); // mult by 4 for float
    float temp_check_sum = 0;
    for (int i = 0; i < rows*cols; i++)
    {
      char char_arr[4];
      char_arr[0] = pixels[i*4];
      char_arr[1] = pixels[i*4+1];
      char_arr[2] = pixels[i*4+2];
      char_arr[3] = pixels[i*4+3];
      float tf =  char_arr_2_float(char_arr);
      if (tf > 100 || tf < -100)
      {
	  LOG(WARNING) << "invalid float likely: " << tf;
      }
      temp_check_sum += tf;

      // add the float data to the datum
      datumFloatData->Add(tf);
    }
    
    if (temp_check_sum < 0.0000001 && temp_check_sum > 0)
    {
      LOG(WARNING) << "float sum for this vector is probably zero: " << temp_check_sum;
    }

    // check the size of the float repeated field
    //LOG(INFO) << "Size of float field " << datumFloatData->size() << "datum: " << datum.float_data_size();
    
    label_file.read(&label, 1); 
    //datum.set_data(pixels, rows*cols); // set above using pointer
    datum.set_label(label);
    string key_str = caffe::format_int(item_id, 8);
    datum.SerializeToString(&value);
    datum.Clear(); // now that it has been serialized we can clear the data
    
    // insert data into the database
    txn->Put(key_str, value);

    if (++count % 1000 == 0) {
      txn->Commit();
    }
  }
  // write the last batch
  if (count % 1000 != 0) {
      txn->Commit();
  }
  LOG(INFO) << "Processed " << count << " files.";
  delete[] pixels;
  db->Close();
}

int main(int argc, char** argv) {
#ifndef GFLAGS_GFLAGS_H_
  namespace gflags = google;
#endif

  FLAGS_alsologtostderr = 1;

  gflags::SetUsageMessage("This script converts the MNIST dataset to\n"
        "the lmdb/leveldb format used by Caffe to load data.\n"
        "Usage:\n"
        "    convert_mnist_data [FLAGS] input_image_file input_label_file "
        "output_db_file\n"
        "The MNIST dataset could be downloaded at\n"
        "    http://yann.lecun.com/exdb/mnist/\n"
        "You should gunzip them after downloading,"
        "or directly use data/mnist/get_mnist.sh\n");
  gflags::ParseCommandLineFlags(&argc, &argv, true);

  const string& db_backend = FLAGS_backend;

  if (argc != 4) {
    gflags::ShowUsageWithFlagsRestrict(argv[0],
        "examples/mnist/convert_mnist_data");
  } else {
    google::InitGoogleLogging(argv[0]);
    convert_dataset(argv[1], argv[2], argv[3], db_backend);
  }
  return 0;
}
#else
int main(int argc, char** argv) {
  LOG(FATAL) << "This example requires LevelDB and LMDB; " <<
  "compile with USE_LEVELDB and USE_LMDB.";
}
#endif  // USE_LEVELDB and USE_LMDB
