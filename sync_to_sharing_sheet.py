import os

# 每次最多操作 10 行数据
MAX_CONCURRENCY = 10


def sync_to_sharing_sheet(dst_imdb, dst_sharing):

  # 获取数据库 top 250 的记录
  records_ready_to_insert = dst_imdb.records.all(viewId=os.environ['TOP_VIEW_ID'])

  # 过期的排行记录
  old_records = dst_sharing.records.all()

  record_ids = ([_._id for _ in old_records])
  # 批量删除
  for index in range(int(len(old_records) / MAX_CONCURRENCY)):
    dst_sharing.delete_records(record_ids[index * MAX_CONCURRENCY: index * MAX_CONCURRENCY + MAX_CONCURRENCY])

  updated_records = [
    {
      "fldi7UMotAQAZ": str(_.rank),
      "fldl2lZN3gtGJ": _.chi_name,
      "fldr1y9gSuWHw": _.eng_name,
      "fldaeorshjgAA": _.director,
      "fldxXVyxowssy": _.year,
      "fldWf1xPvKCiz": _.seen,
    } for _ in records_ready_to_insert
  ]

  for index in range(int(len(updated_records) / MAX_CONCURRENCY)):
    dst_sharing.records.bulk_create(updated_records[index * MAX_CONCURRENCY: index * MAX_CONCURRENCY + MAX_CONCURRENCY])
