var bucketName = 'bucketName';
var bucketRegion = 'bucketRegion';
var IdentityPoolId = 'IdentityPoolId';

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});

var s3 = new AWS.S3({
  apiVersion: '2006-03-01',
  params: {Bucket: bucketName}
});

function addFile() {
  var files = document.getElementById('upload').files;
  if (!files.length) {
    return alert('画像が選択されていません');
  }
  var file = files[0];
  var fileName = getUniqueStr() + "." + getExtension(file.name);
  var folderKey = encodeURIComponent("upload_file") + '/';

  var fileKey = folderKey + fileName;
  s3.upload({
    Key: fileKey,
    Body: file,
    ACL: 'public-read'
  }, function(err, data) {
    if (err) {
      return alert('画像アップロードに失敗しました: ', err.message);
    }
    alert('アップロード成功！');
  });
}

function getUniqueStr(myStrong){
  var strong = 1000;
  if (myStrong) strong = myStrong;
  return new Date().getTime().toString(16) + Math.floor(strong*Math.random()).toString(16);
}

function getExtension(fileName) {
  var ret;
  if (!fileName) {
    return ret;
  }
  var fileTypes = fileName.split(".");
  var len = fileTypes.length;
  if (len === 0) {
    return ret;
  }
  ret = fileTypes[len - 1];
  return ret;
}
