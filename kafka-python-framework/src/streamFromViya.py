from viya_utils import viyaStartUp, kafkaStartUp, produce_object_detections, getTableName

def main():
    viya_params = viyaStartUp()
    producer = kafkaStartUp()
    produce_object_detections(viya_params[0],table= getTableName(viya_params[1]),coord_type='yolo',producerApp=producer)

if __name__ == '__main__':
    main()
